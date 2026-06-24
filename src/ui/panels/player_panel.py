"""
Kraftbeat Global Player Panel

Handles audio playback, waveform visualization, effects processing, and exporting.
Designed to be a persistent bottom dock used by all generation engines.
"""

import logging
import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider,
    QComboBox, QGroupBox, QLineEdit, QFileDialog, QMessageBox, QFrame,
    QStyle, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon

# Optional dependencies
try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

try:
    import pyqtgraph as pg
    PYQTGRAPH_AVAILABLE = True
except ImportError:
    PYQTGRAPH_AVAILABLE = False

from src.utils.audio import normalize_audio, save_audio
from src.utils.effects import apply_effects_chain
from src.utils.config import get_config

logger = logging.getLogger(__name__)


class PlayerPanel(QWidget):
    """
    Global player with Waveform, Playback Controls, Effects, and Export.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_audio = None
        self.current_sample_rate = 32000
        self.is_playing = False
        
        # UI State
        self.volume = 0.8
        self.loop_enabled = False
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # 1. Waveform Area
        self.waveform_frame = QFrame()
        self.waveform_frame.setMinimumHeight(120)
        self.waveform_frame.setStyleSheet("background-color: #252530; border-radius: 6px; border: 1px solid #404050;")
        
        if PYQTGRAPH_AVAILABLE:
            wf_layout = QVBoxLayout(self.waveform_frame)
            wf_layout.setContentsMargins(0, 0, 0, 0)
            self.waveform_plot = pg.PlotWidget()
            self.waveform_plot.setBackground('#252530')
            self.waveform_plot.hideAxis('bottom')
            self.waveform_plot.hideAxis('left')
            self.waveform_plot.setMouseEnabled(x=False, y=False)
            self.waveform_curve = self.waveform_plot.plot(pen=pg.mkPen('#648cff', width=1))
            wf_layout.addWidget(self.waveform_plot)
        else:
            wf_layout = QVBoxLayout(self.waveform_frame)
            self.waveform_label = QLabel("Waveform (install pyqtgraph for visual)")
            self.waveform_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.waveform_label.setStyleSheet("color: #606070;")
            wf_layout.addWidget(self.waveform_label)
            
        layout.addWidget(self.waveform_frame)
        
        # 2. Main Controls Row (Transport + Tabs toggle)
        controls_row = QHBoxLayout()
        controls_row.setContentsMargins(0, 4, 0, 0)
        
        # Play/Stop
        self.play_btn = QPushButton("▶")
        self.play_btn.setFixedSize(40, 40)
        self.play_btn.setStyleSheet("""
            QPushButton { font-size: 20px; border-radius: 20px; background-color: #648cff; border: none; }
            QPushButton:hover { background-color: #7a9fff; }
            QPushButton:disabled { background-color: #404050; color: #606070; }
        """)
        self.play_btn.setEnabled(False)
        self.play_btn.clicked.connect(self.toggle_playback)
        controls_row.addWidget(self.play_btn)
        
        self.stop_btn = QPushButton("⏹")
        self.stop_btn.setFixedSize(36, 36)
        self.stop_btn.setStyleSheet("QPushButton { font-size: 16px; border-radius: 18px; background-color: #404050; border: none; } QPushButton:hover { background-color: #505060; }")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_audio)
        controls_row.addWidget(self.stop_btn)
        
        # Time / Slider
        self.time_label = QLabel("0:00")
        self.time_label.setFixedWidth(40)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        controls_row.addWidget(self.time_label)
        
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setRange(0, 100)
        self.position_slider.setEnabled(False)
        controls_row.addWidget(self.position_slider)
        
        self.duration_label = QLabel("0:00")
        self.duration_label.setFixedWidth(40)
        controls_row.addWidget(self.duration_label)
        
        # Extras (Loop, Volume, Tools)
        controls_row.addSpacing(10)
        
        self.loop_btn = QPushButton("🔁")
        self.loop_btn.setCheckable(True)
        self.loop_btn.setFixedSize(30, 30)
        self.loop_btn.setToolTip("Loop Playback")
        self.loop_btn.clicked.connect(self.toggle_loop)
        controls_row.addWidget(self.loop_btn)
        
        controls_row.addWidget(QLabel("🔊"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setFixedWidth(80)
        self.volume_slider.valueChanged.connect(self.update_volume)
        controls_row.addWidget(self.volume_slider)
        
        # Toggle Effects/Export Panel Button
        self.tools_btn = QPushButton("🎛️ Effects & Export")
        self.tools_btn.setCheckable(True)
        self.tools_btn.setChecked(True)
        self.tools_btn.clicked.connect(self.toggle_tools_panel)
        controls_row.addWidget(self.tools_btn)
        
        layout.addLayout(controls_row)
        
        # 3. Collapsible Tools Panel (Effects + Export)
        self.tools_panel = QFrame()
        self.tools_panel.setStyleSheet("background-color: #1e1e24; border-top: 1px solid #303040; margin-top: 4px;")
        tools_layout = QHBoxLayout(self.tools_panel)
        tools_layout.setContentsMargins(4, 8, 4, 4)
        
        # --- Effects Section ---
        effects_group = QGroupBox("Effects Chain")
        eff_layout = QHBoxLayout(effects_group)
        eff_layout.setContentsMargins(8, 8, 8, 8)
        
        # EQ
        eq_layout = QVBoxLayout()
        eq_layout.addWidget(QLabel("Bass"))
        self.bass_slider = QSlider(Qt.Orientation.Vertical)
        self.bass_slider.setRange(-12, 12)
        self.bass_slider.setValue(0)
        eq_layout.addWidget(self.bass_slider, 0, Qt.AlignmentFlag.AlignHCenter)
        eff_layout.addLayout(eq_layout)
        
        eq_layout2 = QVBoxLayout()
        eq_layout2.addWidget(QLabel("Treble"))
        self.treble_slider = QSlider(Qt.Orientation.Vertical)
        self.treble_slider.setRange(-12, 12)
        self.treble_slider.setValue(0)
        eq_layout2.addWidget(self.treble_slider, 0, Qt.AlignmentFlag.AlignHCenter)
        eff_layout.addLayout(eq_layout2)
        
        # Reverb
        rev_layout = QVBoxLayout()
        rev_layout.addWidget(QLabel("Reverb"))
        self.reverb_slider = QSlider(Qt.Orientation.Vertical)
        self.reverb_slider.setRange(0, 100)
        rev_layout.addWidget(self.reverb_slider, 0, Qt.AlignmentFlag.AlignHCenter)
        eff_layout.addLayout(rev_layout)
        
        # Comp
        comp_layout = QVBoxLayout()
        comp_layout.addWidget(QLabel("Comp"))
        self.compression_slider = QSlider(Qt.Orientation.Vertical)
        self.compression_slider.setRange(0, 100)
        comp_layout.addWidget(self.compression_slider, 0, Qt.AlignmentFlag.AlignHCenter)
        eff_layout.addLayout(comp_layout)
        
        tools_layout.addWidget(effects_group)
        
        # --- Export Section ---
        export_group = QGroupBox("Export")
        exp_layout = QVBoxLayout(export_group)
        
        form_row = QHBoxLayout()
        self.format_combo = QComboBox()
        self.format_combo.addItems(["WAV", "MP3", "FLAC", "OGG"])
        self.format_combo.currentTextChanged.connect(self.update_bitrate_visibility)
        form_row.addWidget(self.format_combo)
        
        self.bitrate_combo = QComboBox()
        self.bitrate_combo.addItems(["128k", "192k", "256k", "320k"])
        self.bitrate_combo.setCurrentText("192k")
        form_row.addWidget(self.bitrate_combo)
        exp_layout.addLayout(form_row)
        
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Notes / Tags...")
        exp_layout.addWidget(self.notes_input)
        
        self.save_btn = QPushButton("💾 Save to File")
        self.save_btn.setStyleSheet("background-color: #50c050; color: white; font-weight: bold; padding: 6px;")
        self.save_btn.clicked.connect(self.save_audio)
        self.save_btn.setEnabled(False)
        exp_layout.addWidget(self.save_btn)
        
        exp_layout.addStretch()
        tools_layout.addWidget(export_group)
        
        layout.addWidget(self.tools_panel)
        
    def set_audio(self, audio, sample_rate):
        """Set the audio data to play/visualize."""
        if audio is None: return
        
        # Update state
        self.current_audio = audio
        self.current_sample_rate = sample_rate
        
        # Update Waveform
        self.update_waveform()
        
        # Update Controls
        duration = audio.shape[-1] / sample_rate
        mins = int(duration // 60)
        secs = int(duration % 60)
        self.duration_label.setText(f"{mins}:{secs:02d}")
        
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.position_slider.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.position_slider.setValue(0)
        self.time_label.setText("0:00")
        
    def update_waveform(self):
        """Draw waveform on plot."""
        if not PYQTGRAPH_AVAILABLE or not hasattr(self, 'waveform_curve'):
            if hasattr(self, 'waveform_label'):
                self.waveform_label.setText("✓ Audio Loaded")
            return
            
        audio = self.current_audio
        # Flatten to mono for display
        if audio.ndim > 1:
            display_audio = audio[0] if audio.shape[0] <= 2 else audio.mean(axis=0)
        else:
            display_audio = audio
            
        # Downsample for perf
        max_points = get_config("waveform_point_limit", 5000)
        if len(display_audio) > max_points:
            step = len(display_audio) // max_points
            display_audio = display_audio[::step]
            
        self.waveform_curve.setData(display_audio)

    def toggle_playback(self):
        """Play or pause audio."""
        if self.current_audio is None: return
        
        if self.is_playing:
            self.stop_audio()
        else:
            self.play_audio()
            
    def play_audio(self):
        if not AUDIO_AVAILABLE:
            return
            
        try:
            # Stop existing
            sd.stop()
            
            # Apply effects real-time? For now, play raw audio to avoid lag, 
            # OR applying effects before play takes time.
            # Ideally: Apply effects once and cache, or apply on save only.
            # Current design: Preview is RAW, Save is PROCESSED (standard for generation apps to be fast).
            # BUT user wants to HEAR effects.
            # Fast compromise: Apply effects to a copy.
            
            audio_to_play = self.get_processed_audio()
            
            # Format for sounddevice (samples, channels)
            if audio_to_play.ndim > 1:
                audio_to_play = audio_to_play.T
                
            self.is_playing = True
            self.play_btn.setText("⏸")
            
            # Play
            sd.play(audio_to_play, self.current_sample_rate, loop=self.loop_enabled)
            
        except Exception as e:
            logger.error(f"Playback error: {e}")
            self.is_playing = False
            self.play_btn.setText("▶")
            
    def stop_audio(self):
        if AUDIO_AVAILABLE:
            sd.stop()
        self.is_playing = False
        self.play_btn.setText("▶")
        
    def toggle_loop(self):
        self.loop_enabled = not self.loop_enabled
        if self.is_playing and AUDIO_AVAILABLE:
            # Restart with new loop setting
            self.play_audio()
            
    def update_volume(self):
        self.volume = self.volume_slider.value() / 100.0
        # SD doesn't have live volume, would need to multiply stream. 
        # For simple sd.play, we can't change vol without restart.
        # Just accept this limitation or restart.
        logger.debug(f"Volume updated to {self.volume:.2f} (applies to next playback)")

    def toggle_tools_panel(self):
        self.tools_panel.setVisible(self.tools_btn.isChecked())
        
    def update_bitrate_visibility(self, text):
        self.bitrate_combo.setEnabled(text in ["MP3", "OGG"])
        
    def get_processed_audio(self):
        """Apply current slider effects to audio copy."""
        if self.current_audio is None: return None
        
        # Get values
        rev = self.reverb_slider.value() / 100.0
        comp = self.compression_slider.value()
        bass = float(self.bass_slider.value())
        treble = float(self.treble_slider.value())
        
        # If no effects
        if rev == 0 and comp == 0 and bass == 0 and treble == 0:
            return self.current_audio
            
        # Apply
        try:
            processed = apply_effects_chain(
                self.current_audio.copy(),
                self.current_sample_rate,
                reverb_wet=rev,
                compression_ratio=1.0 + (comp/20.0), # 1-6 ratio
                eq_bass=bass,
                eq_treble=treble
            )
            return processed
        except Exception as e:
            logger.error(f"Effect processing failed: {e}")
            return self.current_audio

    def save_audio(self):
        if self.current_audio is None: return
        
        fmt = self.format_combo.currentText().lower()
        bitrate = self.bitrate_combo.currentText()
        
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Audio", f"output.{fmt}", f"{fmt.upper()} Files (*.{fmt})"
        )
        
        if path:
            # Process
            final_audio = self.get_processed_audio()
            final_audio = normalize_audio(final_audio)
            
            save_audio(final_audio, path, self.current_sample_rate, fmt, bitrate)
