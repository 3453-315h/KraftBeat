"""
Kraftbeat - Stems Panel

Multi-track stem generation panel for building tracks layer by layer.
Each stem has its own prompt, generation, and mixing controls.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QSlider, QGroupBox, QScrollArea, QFrame,
    QFileDialog, QMessageBox, QProgressDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
import numpy as np
from pathlib import Path
from utils.stems import separate_file
from utils.audio import load_audio

try:
    import pyqtgraph as pg
    PYQTGRAPH_AVAILABLE = True
except ImportError:
    PYQTGRAPH_AVAILABLE = False


class StemTrack(QFrame):
    """Individual stem track with prompt, controls, and waveform."""
    
    generate_requested = pyqtSignal(str, str)  # stem_name, prompt
    
    # Color scheme for different stem types
    COLORS = {
        "🥁 Drums": "#4a7cb0",      # Blue
        "🎸 Bass": "#8b5a3c",        # Brown
        "🎹 Instruments": "#9b6b9b",  # Purple
        "🎤 Vocals": "#7ab07a",       # Green
        "🎵 Synth": "#bf7f3f",        # Orange
        "🎺 Brass": "#c06050",        # Red
    }
    
    DEFAULT_PROMPTS = {
        "🥁 Drums": "drum beat, percussion, rhythm, crisp hi-hats",
        "🎸 Bass": "bass line, low frequency, groovy, deep",
        "🎹 Instruments": "melodic instruments, harmony, piano, guitar",
        "🎤 Vocals": "vocal melody, choir, harmonies, ethereal",
        "🎵 Synth": "synthesizer, electronic, ambient pads",
        "🎺 Brass": "brass section, horns, trumpet, saxophone",
    }
    
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self.name = name
        self.audio_data = None
        self.sample_rate = 32000
        self.is_muted = False
        self.is_solo = False
        self.volume = 0.8
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the stem track UI."""
        color = self.COLORS.get(self.name, "#505060")
        
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet(f"""
            StemTrack {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}40, stop:1 {color}20);
                border: 2px solid {color};
                border-radius: 8px;
                margin: 2px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Left section: track info and controls
        left_section = QVBoxLayout()
        left_section.setSpacing(4)
        
        # Track name label
        name_label = QLabel(self.name)
        name_label.setStyleSheet(f"font-weight: bold; color: {color}; font-size: 14px;")
        left_section.addWidget(name_label)
        
        # Mute/Solo buttons row
        btn_row = QHBoxLayout()
        
        self.mute_btn = QPushButton("M")
        self.mute_btn.setToolTip("Mute")
        self.mute_btn.setCheckable(True)
        self.mute_btn.setMaximumWidth(30)
        self.mute_btn.setStyleSheet("""
            QPushButton { background: #404050; border-radius: 4px; }
            QPushButton:checked { background: #c04040; }
        """)
        self.mute_btn.clicked.connect(self.toggle_mute)
        btn_row.addWidget(self.mute_btn)
        
        self.solo_btn = QPushButton("S")
        self.solo_btn.setToolTip("Solo")
        self.solo_btn.setCheckable(True)
        self.solo_btn.setMaximumWidth(30)
        self.solo_btn.setStyleSheet("""
            QPushButton { background: #404050; border-radius: 4px; }
            QPushButton:checked { background: #c0a040; }
        """)
        self.solo_btn.clicked.connect(self.toggle_solo)
        btn_row.addWidget(self.solo_btn)
        
        btn_row.addStretch()
        left_section.addLayout(btn_row)
        
        # Volume slider
        vol_row = QHBoxLayout()
        vol_row.addWidget(QLabel("🔊"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setMaximumWidth(60)
        self.volume_slider.valueChanged.connect(self.on_volume_change)
        vol_row.addWidget(self.volume_slider)
        left_section.addLayout(vol_row)
        
        layout.addLayout(left_section)
        
        # Middle section: prompt and generate
        middle_section = QVBoxLayout()
        
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText(self.DEFAULT_PROMPTS.get(self.name, "Enter stem prompt..."))
        self.prompt_input.setStyleSheet("padding: 6px; border-radius: 4px;")
        middle_section.addWidget(self.prompt_input)
        
        self.generate_btn = QPushButton("🎵 Generate")
        self.generate_btn.setStyleSheet(f"background: {color}; padding: 8px;")
        self.generate_btn.clicked.connect(self.on_generate)
        
        self.midi_btn = QPushButton("🎹 MIDI")
        self.midi_btn.setToolTip("Export to MIDI (requires basic-pitch)")
        self.midi_btn.setStyleSheet("padding: 8px; background: #404050;")
        self.midi_btn.clicked.connect(self.on_midi_export)
        
        action_layout = QHBoxLayout()
        action_layout.addWidget(self.generate_btn, stretch=3)
        action_layout.addWidget(self.midi_btn, stretch=1)
        middle_section.addLayout(action_layout)
        
        layout.addLayout(middle_section, stretch=2)
        
        # Right section: waveform display
        if PYQTGRAPH_AVAILABLE:
            self.waveform = pg.PlotWidget()
            self.waveform.setBackground(None)
            self.waveform.setMinimumWidth(200)
            self.waveform.setMaximumHeight(60)
            self.waveform.hideAxis('bottom')
            self.waveform.hideAxis('left')
            self.waveform.setMouseEnabled(False, False)
            layout.addWidget(self.waveform, stretch=3)
        else:
            self.waveform = QLabel("📊 Waveform")
            self.waveform.setStyleSheet("color: #606070; font-style: italic;")
            layout.addWidget(self.waveform, stretch=3)
        
        # Status indicator
        self.status_label = QLabel("⚪ Empty")
        self.status_label.setStyleSheet("color: #707080; font-size: 10px;")
        layout.addWidget(self.status_label)
        
    def toggle_mute(self):
        """Toggle mute state."""
        self.is_muted = self.mute_btn.isChecked()
        
    def toggle_solo(self):
        """Toggle solo state."""
        self.is_solo = self.solo_btn.isChecked()
        
    def on_volume_change(self, value):
        """Handle volume slider change."""
        self.volume = value / 100.0
        
    def on_generate(self):
        """Request generation for this stem."""
        prompt = self.prompt_input.text().strip()
        if not prompt:
            prompt = self.DEFAULT_PROMPTS.get(self.name, "")
        self.status_label.setText("🟡 Generating...")
        self.generate_requested.emit(self.name, prompt)
        
    def on_midi_export(self):
        """Export audio to MIDI."""
        if self.audio_data is None:
            QMessageBox.warning(self, "Warning", "No audio generated for this stem yet.")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, f"Export {self.name} to MIDI", f"stem_midi.mid", 
            "MIDI Files (*.mid)"
        )
        if not file_path:
            return
            
        self.status_label.setText("🟡 Extracting MIDI...")
        
        # Save temp audio file
        from utils.audio import save_audio
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name
            
        save_audio(self.audio_data, temp_path, self.sample_rate)
        
        # Extract MIDI
        from utils.midi import audio_to_midi
        res = audio_to_midi(temp_path, file_path)
        
        try:
            os.remove(temp_path)
        except Exception as e:
            logger.debug(f"Failed to remove temporary file {temp_path}: {e}")
            
        if res:
            self.status_label.setText("🟢 MIDI Saved")
            QMessageBox.information(self, "Success", f"MIDI exported to {file_path}")
        else:
            self.status_label.setText("🔴 MIDI Failed")
            QMessageBox.warning(self, "Failed", "Could not extract MIDI. Is basic-pitch installed?")
        
    def set_audio(self, audio_data: np.ndarray, sample_rate: int):
        """Set the audio data for this stem."""
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        self.status_label.setText("🟢 Ready")
        self.update_waveform()
        
    def update_waveform(self):
        """Update waveform display."""
        if not PYQTGRAPH_AVAILABLE or self.audio_data is None:
            return
            
        # Downsample for display
        samples = min(1000, len(self.audio_data))
        indices = np.linspace(0, len(self.audio_data) - 1, samples).astype(int)
        display_data = self.audio_data[indices]
        
        color = self.COLORS.get(self.name, "#648cff")
        self.waveform.clear()
        self.waveform.plot(display_data, pen=pg.mkPen(color, width=1))
        
    def get_mixed_audio(self) -> np.ndarray:
        """Get audio data with volume applied, respecting mute."""
        if self.audio_data is None or self.is_muted:
            return None
        return self.audio_data * self.volume


class SeparationWorker(QThread):
    """Background worker for stem separation."""
    finished = pyqtSignal(object)  # dict or None
    error = pyqtSignal(str)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        
    def run(self):
        try:
            # Use same directory for output
            output_dir = str(Path(self.file_path).parent / "stems")
            results = separate_file(self.file_path, output_dir=output_dir)
            if results:
                self.finished.emit(results)
            else:
                self.error.emit("Separation failed (check if Demucs is installed)")
        except Exception as e:
            self.error.emit(str(e))


class StemsPanel(QWidget):
    """Main stems panel with multiple track layers."""
    
    # Signal to request generation: (track_index, prompt, duration)
    stem_generation_needed = pyqtSignal(int, str, float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tracks = []
        self.duration = 8  # All stems same duration
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the stems panel UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("🎚️ Stems Mixer")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        
        # Duration control
        header.addWidget(QLabel("Duration:"))
        from PyQt6.QtWidgets import QSpinBox
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(4, 30)
        self.duration_spin.setValue(8)
        self.duration_spin.setSuffix("s")
        self.duration_spin.valueChanged.connect(self.on_duration_change)
        header.addWidget(self.duration_spin)
        
        layout.addLayout(header)
        
        # Scroll area for tracks
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        tracks_widget = QWidget()
        self.tracks_layout = QVBoxLayout(tracks_widget)
        self.tracks_layout.setSpacing(4)
        
        # Create default stems
        stem_names = ["🥁 Drums", "🎸 Bass", "🎹 Instruments", "🎤 Vocals", "🎵 Synth"]
        for name in stem_names:
            self.add_stem_track(name)
            
        self.tracks_layout.addStretch()
        scroll.setWidget(tracks_widget)
        layout.addWidget(scroll, stretch=1)
        
        # Bottom controls
        controls = QHBoxLayout()
        
        self.add_track_btn = QPushButton("➕ Add Track")
        self.add_track_btn.clicked.connect(self.add_new_track)
        controls.addWidget(self.add_track_btn)
        
        self.import_btn = QPushButton("📂 Import & Separate")
        self.import_btn.setToolTip("Import audio file and split into stems")
        self.import_btn.clicked.connect(self.import_and_separate)
        controls.addWidget(self.import_btn)
        
        controls.addStretch()
        
        self.generate_all_btn = QPushButton("🎵 Generate All")
        self.generate_all_btn.setStyleSheet("background: #50a050; padding: 10px 20px;")
        self.generate_all_btn.clicked.connect(self.generate_all_stems)
        controls.addWidget(self.generate_all_btn)
        
        self.mix_btn = QPushButton("🎚️ Mix & Export")
        self.mix_btn.setStyleSheet("background: #648cff; padding: 10px 20px;")
        self.mix_btn.clicked.connect(self.mix_and_export)
        controls.addWidget(self.mix_btn)
        
        layout.addLayout(controls)
        
    def add_stem_track(self, name: str):
        """Add a stem track to the panel."""
        track = StemTrack(name)
        track.generate_requested.connect(self.on_stem_generate_requested)
        self.tracks.append(track)
        self.tracks_layout.insertWidget(self.tracks_layout.count() - 1, track)
        
    def add_new_track(self):
        """Add a new custom track."""
        # Cycle through available track types
        available = ["🎺 Brass", "🪕 Strings", "🎻 Orchestra", "🔔 Percussion"]
        used_names = [t.name for t in self.tracks]
        for name in available:
            if name not in used_names:
                self.add_stem_track(name)
                return
        # If all used, add numbered custom track
        self.add_stem_track(f"🎵 Custom {len(self.tracks) + 1}")
        
    def on_duration_change(self, value):
        """Handle duration change."""
        self.duration = value
        
    def on_stem_generate_requested(self, stem_name: str, prompt: str):
        """Handle generation request from a stem track."""
        # Find index of the track that requested generation
        sender = self.sender()
        if sender in self.tracks:
            idx = self.tracks.index(sender)
            self.stem_generation_needed.emit(idx, prompt, float(self.duration))
        
    def update_track_audio(self, idx: int, audio: np.ndarray, sr: int):
        """Callback to update a track with generated audio."""
        if 0 <= idx < len(self.tracks):
             self.tracks[idx].set_audio(audio, sr)
        
    def generate_all_stems(self):
        """Generate all stems sequentially."""
        # We trigger them one by one? 
        # For now, let's just trigger the first empty one or all?
        # A cascade logic would be complex here without a queue manager in MainWindow.
        # So we'll just trigger all signals and let MainWindow queue them.
        for i, track in enumerate(self.tracks):
             prompt = track.prompt_input.text().strip() or track.DEFAULT_PROMPTS.get(track.name, "")
             self.stem_generation_needed.emit(i, prompt, float(self.duration))
            
    def mix_and_export(self):
        """Mix all stems and export."""
        # Collect all audio that should be mixed
        mixed_audio = None
        
        # Check for solo tracks
        solo_active = any(t.is_solo for t in self.tracks)
        
        for track in self.tracks:
            audio = track.get_mixed_audio()
            if audio is None:
                continue
                
            # If solo is active, only include solo tracks
            if solo_active and not track.is_solo:
                continue
                
            if mixed_audio is None:
                mixed_audio = audio.copy()
            else:
                # Pad or trim to match lengths
                if len(audio) > len(mixed_audio):
                    mixed_audio = np.pad(mixed_audio, (0, len(audio) - len(mixed_audio)))
                elif len(audio) < len(mixed_audio):
                    audio = np.pad(audio, (0, len(mixed_audio) - len(audio)))
                mixed_audio = mixed_audio + audio
                
        if mixed_audio is not None:
            # Normalize to prevent clipping
            max_val = np.max(np.abs(mixed_audio))
            if max_val > 0:
                mixed_audio = mixed_audio / max_val * 0.9
            
            # Save dialog
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Mix", "mix.wav", 
                "WAV Files (*.wav);;MP3 Files (*.mp3)"
            )
            if file_path:
                from utils.audio import save_audio
                save_audio(mixed_audio, file_path, 32000) # Assuming 32kHz
                QMessageBox.information(self, "Success", f"Mix saved to {file_path}")
        else:
            QMessageBox.warning(self, "Warning", "No audio to mix")

    def import_and_separate(self):
        """Import file and separate into stems."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Audio File", "", 
            "Audio Files (*.wav *.mp3 *.flac *.ogg)"
        )
        
        if not file_path:
            return
            
        # Show progress
        self.progress = QProgressDialog("Separating stems (check console for details)...", "Cancel", 0, 0, self)
        self.progress.setWindowTitle("Please Wait")
        self.progress.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress.show()
        
        self.worker = SeparationWorker(file_path)
        self.worker.finished.connect(self.on_separation_complete)
        self.worker.error.connect(self.on_separation_error)
        self.worker.start()
        
    def on_separation_error(self, error):
        self.progress.close()
        QMessageBox.warning(self, "Separation Failed", error)
        
    def on_separation_complete(self, stems):
        self.progress.close()
        
        # Map demucs names to our track names
        stem_map = {
            'drums': '🥁 Drums',
            'bass': '🎸 Bass',
            'other': '🎹 Instruments',
            'vocals': '🎤 Vocals'
        }
        
        # Add to matching tracks
        count = 0
        for stem_key, file_path in stems.items():
            track_name = stem_map.get(stem_key)
            if not track_name:
                continue
                
            # Load audio
            res = load_audio(file_path, target_sr=32000) # Force 32kHz for consistency
            if res is None:
                continue
            audio, sr = res
            
            # Find track
            track = next((t for t in self.tracks if t.name == track_name), None)
            if not track:
                self.add_stem_track(track_name)
                track = self.tracks[-1]
            
            track.set_audio(audio, sr)
            count += 1
            
        if count > 0:
            QMessageBox.information(self, "Success", f"Separated into {len(stems)} stems!")
        else:
            QMessageBox.warning(self, "Warning", "No matching stems found or loaded.")


# For testing
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    panel = StemsPanel()
    panel.resize(800, 600)
    panel.show()
    sys.exit(app.exec())
