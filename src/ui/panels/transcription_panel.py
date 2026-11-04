"""
NeuralNote Native Transcription View for KraftBeat.

Recreates the NeuralNote layout and interaction model in PyQt6:
- Waveform display on top with synchronized playhead
- High-performance piano roll canvas with keyboard gutter, pitch grid, and instrument-colored notes
- Left sidebar with per-instrument strips (color chip, note count, pitch range, gain, mute/solo)
- Transport controls and MIDI drag-and-drop export
- Status bar displaying duration, tempo, pitch range, and placeholder tempo grid flags
"""

import logging
from pathlib import Path
from typing import Optional, Dict, List
import numpy as np

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QScrollArea, QFrame, QSplitter, QFileDialog,
    QMessageBox, QDialog, QToolButton
)
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal, QTimer, QMimeData, QUrl
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QDrag

from src.models.transcription import TranscriptionResult, TranscriptionNote

logger = logging.getLogger(__name__)

# Consistent color palette for instrument separation (NeuralNote dark aesthetic)
INSTRUMENT_COLORS = [
    QColor(76, 175, 80),    # Emerald Green (Piano)
    QColor(33, 150, 243),   # Azure Blue (Bass)
    QColor(255, 152, 0),    # Amber Orange (Guitar)
    QColor(233, 30, 99),    # Vivid Pink (Drums/Percussion)
    QColor(156, 39, 176),   # Royal Purple (Strings)
    QColor(0, 188, 212),    # Cyan (Lead Synth)
    QColor(255, 235, 59),   # Yellow (Brass)
    QColor(255, 87, 34),    # Deep Orange (Vocals)
]


class PianoRollCanvas(QWidget):
    """
    Interactive Piano Roll Canvas rendering notes, grid, keyboard gutter, and playhead.
    Supports drag-and-drop export of the MIDI file.
    """
    
    time_clicked = pyqtSignal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(350)
        self.setMinimumWidth(500)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAcceptDrops(False)
        
        self.result: Optional[TranscriptionResult] = None
        self.instrument_colors: Dict[str, QColor] = {}
        self.muted_instruments: set = set()
        self.solo_instruments: set = set()
        
        self.current_time_sec: float = 0.0
        self.total_duration_sec: float = 10.0
        self.min_pitch: int = 36  # C2
        self.max_pitch: int = 84  # C6
        
        self.gutter_width: int = 50
        self.header_height: int = 24
        self._drag_start_pos = None

    def set_result(self, result: TranscriptionResult):
        self.result = result
        if result.notes:
            self.total_duration_sec = max(result.duration, max(n.offset_sec for n in result.notes), 1.0)
            pitches = [n.pitch for n in result.notes]
            self.min_pitch = max(0, min(pitches) - 2)
            self.max_pitch = min(127, max(pitches) + 2)
        else:
            self.total_duration_sec = max(result.duration, 5.0)
            self.min_pitch = 36
            self.max_pitch = 84

        # Assign colors to instruments
        instruments = result.get_instruments()
        self.instrument_colors.clear()
        for i, inst in enumerate(instruments):
            self.instrument_colors[inst] = INSTRUMENT_COLORS[i % len(INSTRUMENT_COLORS)]

        self.muted_instruments.clear()
        self.solo_instruments.clear()
        self.update()

    set_transcription = set_result

    def time_to_x(self, time_sec: float) -> float:
        roll_width = max(1, self.width() - self.gutter_width)
        dur = max(self.total_duration_sec, 0.001)
        return self.gutter_width + (time_sec / dur) * roll_width

    def x_to_time(self, x: float) -> float:
        roll_width = max(1, self.width() - self.gutter_width)
        dur = max(self.total_duration_sec, 0.001)
        return max(0.0, min(dur, ((x - self.gutter_width) / roll_width) * dur))

    def pitch_to_y(self, pitch: int) -> float:
        pitch_count = max(1, self.max_pitch - self.min_pitch + 1)
        row_height = (self.height() - self.header_height) / pitch_count
        pitch_offset = self.max_pitch - pitch
        return self.header_height + pitch_offset * row_height

    def y_to_pitch(self, y: float) -> int:
        pitch_count = max(1, self.max_pitch - self.min_pitch + 1)
        row_height = max(1.0, (self.height() - self.header_height) / pitch_count)
        offset = int((y - self.header_height) / row_height)
        return max(self.min_pitch, min(self.max_pitch, self.max_pitch - offset))

    def is_note_visible(self, note: TranscriptionNote) -> bool:
        if self.solo_instruments and note.instrument not in self.solo_instruments:
            return False
        if note.instrument in self.muted_instruments:
            return False
        return True

    def set_instrument_mute(self, instrument: str, muted: bool):
        if muted:
            self.muted_instruments.add(instrument)
        else:
            self.muted_instruments.discard(instrument)
        self.update()

    def set_instrument_solo(self, instrument: str, solo: bool):
        if solo:
            self.solo_instruments.add(instrument)
        else:
            self.solo_instruments.discard(instrument)
        self.update()

    def set_current_time(self, time_sec: float):
        self.current_time_sec = max(0.0, min(time_sec, self.total_duration_sec))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        
        # 1. Dark background
        painter.fillRect(0, 0, w, h, QColor(18, 18, 22))

        pitch_count = max(1, self.max_pitch - self.min_pitch + 1)
        row_height = (h - self.header_height) / pitch_count
        roll_width = w - self.gutter_width

        # 2. Draw Pitch Rows and Gutter
        font = QFont("sans-serif", 8)
        painter.setFont(font)

        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        for idx, pitch in enumerate(range(self.max_pitch, self.min_pitch - 1, -1)):
            y = self.header_height + idx * row_height
            is_black_key = (pitch % 12) in (1, 3, 6, 8, 10)
            
            # Row background
            row_bg = QColor(24, 24, 28) if is_black_key else QColor(30, 30, 35)
            painter.fillRect(QRectF(self.gutter_width, y, roll_width, row_height), row_bg)
            
            # Row separator line
            painter.setPen(QPen(QColor(40, 40, 48), 1))
            painter.drawLine(int(self.gutter_width), int(y + row_height), int(w), int(y + row_height))

            # Piano key in gutter
            key_color = QColor(35, 35, 40) if is_black_key else QColor(220, 220, 225)
            painter.fillRect(QRectF(0, y, self.gutter_width - 2, row_height), key_color)
            
            # Gutter note text
            octave = (pitch // 12) - 1
            name = f"{note_names[pitch % 12]}{octave}"
            text_color = QColor(180, 180, 185) if is_black_key else QColor(30, 30, 35)
            painter.setPen(text_color)
            painter.drawText(QRectF(4, y, self.gutter_width - 8, row_height), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, name)

        # 3. Time Grid & Header
        painter.fillRect(0, 0, w, self.header_height, QColor(28, 28, 34))
        painter.setPen(QPen(QColor(60, 60, 70), 1))
        painter.drawLine(0, self.header_height, w, self.header_height)
        painter.drawLine(self.gutter_width, 0, self.gutter_width, h)

        # Draw 1-second grid divisions
        step_sec = 1.0
        if self.total_duration_sec > 30:
            step_sec = 5.0
        elif self.total_duration_sec > 120:
            step_sec = 10.0

        t = 0.0
        painter.setPen(QColor(150, 150, 160))
        while t <= self.total_duration_sec:
            x = self.gutter_width + (t / self.total_duration_sec) * roll_width
            # Vertical grid line
            painter.setPen(QPen(QColor(45, 45, 55), 1))
            painter.drawLine(int(x), self.header_height, int(x), h)
            # Header label
            painter.setPen(QColor(140, 140, 150))
            painter.drawText(int(x + 3), self.header_height - 6, f"{t:.0f}s")
            t += step_sec

        # 4. Draw Transcribed Note Rectangles
        if self.result and self.result.notes:
            for note in self.result.notes:
                # Visibility filtering (Mute / Solo)
                if self.solo_instruments and note.instrument not in self.solo_instruments:
                    continue
                if note.instrument in self.muted_instruments:
                    continue

                if note.pitch < self.min_pitch or note.pitch > self.max_pitch:
                    continue

                pitch_offset = self.max_pitch - note.pitch
                note_y = self.header_height + pitch_offset * row_height + 1
                note_h = max(2.0, row_height - 2.0)

                x1 = self.gutter_width + (note.onset_sec / self.total_duration_sec) * roll_width
                x2 = self.gutter_width + (note.offset_sec / self.total_duration_sec) * roll_width
                note_w = max(3.0, x2 - x1)

                base_color = self.instrument_colors.get(note.instrument, QColor(100, 180, 240))
                # Slight brightness scaling if velocity is available
                if note.velocity is not None:
                    alpha = int(140 + 115 * (note.velocity / 127.0))
                else:
                    alpha = 230
                fill_color = QColor(base_color.red(), base_color.green(), base_color.blue(), alpha)

                painter.setBrush(QBrush(fill_color))
                painter.setPen(QPen(fill_color.lighter(130), 1))
                painter.drawRoundedRect(QRectF(x1, note_y, note_w, note_h), 2.0, 2.0)

        # 5. Playhead
        if self.total_duration_sec > 0:
            playhead_x = self.gutter_width + (self.current_time_sec / self.total_duration_sec) * roll_width
            painter.setPen(QPen(QColor(255, 60, 60), 2))
            painter.drawLine(int(playhead_x), 0, int(playhead_x), h)
            # Playhead handle
            painter.setBrush(QBrush(QColor(255, 60, 60)))
            poly = [
                QPointF(playhead_x - 5, 0),
                QPointF(playhead_x + 5, 0),
                QPointF(playhead_x, 10),
            ]
            painter.drawPolygon(poly)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = event.pos()
            x = event.position().x()
            if x >= self.gutter_width:
                roll_width = self.width() - self.gutter_width
                click_sec = ((x - self.gutter_width) / roll_width) * self.total_duration_sec
                self.time_clicked.emit(click_sec)
                self.set_current_time(click_sec)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton) or not self._drag_start_pos:
            return
        # If user drags sufficiently far with a result loaded, initiate MIDI file drag-out
        if (event.pos() - self._drag_start_pos).manhattanLength() > 15:
            if self.result and self.result.midi_bytes:
                self._start_midi_drag()

    def _start_midi_drag(self):
        """Initiate drag-out of MIDI file to DAW or OS file manager."""
        import tempfile
        temp_dir = Path(tempfile.gettempdir()) / "kraftbeat_midi"
        temp_dir.mkdir(exist_ok=True)
        midi_path = temp_dir / "transcription.mid"
        self.result.save_midi(str(midi_path))

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setUrls([QUrl.fromLocalFile(str(midi_path))])
        mime_data.setData("audio/midi", self.result.midi_bytes)
        mime_data.setData("application/x-midi", self.result.midi_bytes)
        drag.setMimeData(mime_data)
        drag.exec(Qt.DropAction.CopyAction)


class InstrumentStripWidget(QFrame):
    """Sidebar widget for a single transcribed instrument."""

    toggled_mute = pyqtSignal(str, bool)
    toggled_solo = pyqtSignal(str, bool)

    def __init__(self, instrument_name: str, color: QColor, note_count: int, pitch_range: str, parent=None):
        super().__init__(parent)
        self.instrument_name = instrument_name
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            InstrumentStripWidget {
                background-color: #1e1e24;
                border: 1px solid #2e2e38;
                border-radius: 4px;
                padding: 4px;
                margin-bottom: 4px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        # Header: Color chip + name
        top_layout = QHBoxLayout()
        chip = QLabel()
        chip.setFixedSize(12, 12)
        chip.setStyleSheet(f"background-color: {color.name()}; border-radius: 3px;")
        top_layout.addWidget(chip)

        display_name = instrument_name.replace("_", " ").title()
        name_lbl = QLabel(display_name[:20])
        name_lbl.setStyleSheet("font-weight: bold; color: #ececf1;")
        top_layout.addWidget(name_lbl)
        top_layout.addStretch()
        layout.addLayout(top_layout)

        # Meta: Note count & pitch range
        meta_lbl = QLabel(f"{note_count} notes | {pitch_range}")
        meta_lbl.setStyleSheet("color: #9e9ea8; font-size: 11px;")
        layout.addWidget(meta_lbl)

        # Controls: Mute / Solo
        ctrl_layout = QHBoxLayout()
        self.mute_btn = QPushButton("M")
        self.mute_btn.setCheckable(True)
        self.mute_btn.setFixedSize(24, 22)
        self.mute_btn.setStyleSheet("""
            QPushButton { background-color: #2b2b35; color: #aaa; border: 1px solid #444; border-radius: 3px; font-weight: bold; }
            QPushButton:checked { background-color: #d32f2f; color: white; }
        """)
        self.mute_btn.toggled.connect(lambda checked: self.toggled_mute.emit(self.instrument_name, checked))

        self.solo_btn = QPushButton("S")
        self.solo_btn.setCheckable(True)
        self.solo_btn.setFixedSize(24, 22)
        self.solo_btn.setStyleSheet("""
            QPushButton { background-color: #2b2b35; color: #aaa; border: 1px solid #444; border-radius: 3px; font-weight: bold; }
            QPushButton:checked { background-color: #fbc02d; color: black; }
        """)
        self.solo_btn.toggled.connect(lambda checked: self.toggled_solo.emit(self.instrument_name, checked))

        ctrl_layout.addWidget(self.mute_btn)
        ctrl_layout.addWidget(self.solo_btn)
        ctrl_layout.addStretch()
        layout.addLayout(ctrl_layout)


def synthesize_transcription_audio(
    notes: List[TranscriptionNote],
    duration: float,
    sample_rate: int = 22050,
    muted_instruments: Optional[set] = None,
    solo_instruments: Optional[set] = None,
) -> np.ndarray:
    """Synthesize transcribed notes into a multi-timbral audition stereo waveform."""
    total_samples = int(max(duration, 0.5) * sample_rate)
    audio = np.zeros((total_samples, 2), dtype=np.float32)
    if not notes:
        return audio

    t_step = 1.0 / sample_rate
    for n in notes:
        if solo_instruments and n.instrument not in solo_instruments:
            continue
        if muted_instruments and n.instrument in muted_instruments:
            continue

        start_idx = int(n.onset_sec * sample_rate)
        end_idx = int(n.offset_sec * sample_rate)
        if start_idx >= total_samples or end_idx <= start_idx:
            continue
        end_idx = min(end_idx, total_samples)
        num_samples = end_idx - start_idx

        freq = 440.0 * (2.0 ** ((n.pitch - 69.0) / 12.0))
        t = np.arange(num_samples) * t_step
        phase = 2.0 * np.pi * freq * t

        # Fundamental + 2nd & 3rd harmonics
        tone = np.sin(phase) + 0.4 * np.sin(2.0 * phase) + 0.2 * np.sin(3.0 * phase)

        # 10ms attack, 30ms release envelope
        attack_len = min(int(0.01 * sample_rate), max(1, num_samples // 4))
        release_len = min(int(0.03 * sample_rate), max(1, num_samples // 4))
        env = np.ones(num_samples, dtype=np.float32)
        if attack_len > 0:
            env[:attack_len] = np.linspace(0.0, 1.0, attack_len)
        if release_len > 0:
            env[-release_len:] = np.linspace(1.0, 0.0, release_len)

        tone *= env
        vel = (n.velocity / 127.0) if n.velocity is not None else 0.8
        tone *= (vel * 0.25)

        # Stereo pan based on pitch
        pan = min(max((n.pitch - 36) / 48.0, 0.0), 1.0)
        audio[start_idx:end_idx, 0] += tone * (1.0 - pan)
        audio[start_idx:end_idx, 1] += tone * pan

    # Soft limiter
    max_val = np.max(np.abs(audio))
    if max_val > 0.95:
        audio = (audio / max_val) * 0.95
    return audio


class TranscriptionDialog(QDialog):
    """
    Dedicated NeuralNote Transcription View Dialog with interactive Piano Roll,
    audition note synthesis, and ORIG <-> MIDI blend playback.
    """

    def __init__(self, result: TranscriptionResult, parent=None, midi_path: Optional[str] = None):
        super().__init__(parent)
        self.result = result
        self.midi_path = midi_path
        self.sr = 22050
        self._synth_audio: Optional[np.ndarray] = None
        self._orig_audio: Optional[np.ndarray] = None
        self._is_playing: bool = False
        self._play_start_epoch: float = 0.0
        self._play_offset_sec: float = 0.0

        self.setWindowTitle("KraftBeat Transcription (NeuralNote Engine)")
        self.setMinimumSize(950, 600)
        self.resize(1100, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #121216;
                color: #e0e0e0;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)

        # 1. Top Bar: Transport, Title, Engine label, Blend Slider, Export Button
        top_bar = QHBoxLayout()
        title_lbl = QLabel("🎵 Audio-to-MIDI Transcription")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #fff;")
        top_bar.addWidget(title_lbl)

        top_bar.addSpacing(15)
        self.play_btn = QPushButton("▶ Play")
        self.play_btn.setStyleSheet("background-color: #1976d2; color: white; font-weight: bold; padding: 5px 12px; border-radius: 4px;")
        self.play_btn.clicked.connect(self.toggle_play)
        top_bar.addWidget(self.play_btn)

        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setStyleSheet("background-color: #37474f; color: white; padding: 5px 10px; border-radius: 4px;")
        self.stop_btn.clicked.connect(self.stop_play)
        top_bar.addWidget(self.stop_btn)

        self.time_lbl = QLabel(f"0.0s / {self.result.duration:.1f}s")
        self.time_lbl.setStyleSheet("color: #bbb; font-size: 12px; font-family: monospace; min-width: 90px;")
        top_bar.addWidget(self.time_lbl)

        top_bar.addSpacing(15)
        engine_badge = QLabel(f"Engine: {result.engine_id.upper()}")
        engine_badge.setStyleSheet("background-color: #282834; padding: 4px 8px; border-radius: 4px; color: #64b5f6; font-weight: bold;")
        top_bar.addWidget(engine_badge)

        if result.is_placeholder_grid:
            warning_badge = QLabel("⚠️ Placeholder 120 BPM")
            warning_badge.setStyleSheet("background-color: #4a3800; color: #ffeb3b; padding: 4px 8px; border-radius: 4px;")
            top_bar.addWidget(warning_badge)

        top_bar.addSpacing(15)
        top_bar.addWidget(QLabel("ORIG"))
        self.blend_slider = QSlider(Qt.Orientation.Horizontal)
        self.blend_slider.setRange(0, 100)
        self.blend_slider.setValue(60)
        self.blend_slider.setFixedWidth(90)
        self.blend_slider.setToolTip("ORIG <-> MIDI Synth Audition Blend")
        self.blend_slider.valueChanged.connect(self._on_blend_changed)
        top_bar.addWidget(self.blend_slider)
        top_bar.addWidget(QLabel("MIDI"))

        top_bar.addStretch()

        self.export_btn = QPushButton("💾 Export .mid")
        self.export_btn.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold; padding: 6px 14px; border-radius: 4px;")
        self.export_btn.clicked.connect(self.on_export_midi)
        top_bar.addWidget(self.export_btn)

        drag_hint = QLabel("💡 Drag canvas to drop MIDI into DAW")
        drag_hint.setStyleSheet("color: #888; font-size: 11px;")
        top_bar.addWidget(drag_hint)

        main_layout.addLayout(top_bar)

        # 2. Main Content Splitter (Sidebar + Piano Roll)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: #2a2a34; }")

        # Sidebar with Instrument strips
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(0, 0, 4, 0)
        sidebar_layout.setSpacing(4)

        sidebar_title = QLabel("TRACKS / INSTRUMENTS")
        sidebar_title.setStyleSheet("color: #777; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        sidebar_layout.addWidget(sidebar_title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_content = QWidget()
        self.strips_layout = QVBoxLayout(scroll_content)
        self.strips_layout.setContentsMargins(0, 0, 0, 0)
        self.strips_layout.setSpacing(4)

        # Add strip for each instrument
        self.piano_roll = PianoRollCanvas(self)
        self.piano_roll.set_result(self.result)
        self.piano_roll.time_clicked.connect(self.seek_to)

        self.instrument_strips = {}
        instruments = result.get_instruments()
        for inst in instruments:
            notes = result.get_notes_for_instrument(inst)
            pitches = [n.pitch for n in notes]
            p_min, p_max = min(pitches), max(pitches)
            p_range = f"{p_min} - {p_max}"
            color = self.piano_roll.instrument_colors.get(inst, QColor(100, 180, 240))

            strip = InstrumentStripWidget(inst, color, len(notes), p_range)
            strip.toggled_mute.connect(self.on_mute_toggled)
            strip.toggled_solo.connect(self.on_solo_toggled)
            self.instrument_strips[inst] = strip
            self.strips_layout.addWidget(strip)

        self.strips_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        sidebar_layout.addWidget(scroll_area)
        sidebar_widget.setMinimumWidth(200)
        sidebar_widget.setMaximumWidth(280)

        splitter.addWidget(sidebar_widget)
        splitter.addWidget(self.piano_roll)
        splitter.setStretchFactor(1, 4)

        main_layout.addWidget(splitter)

        # 3. Status Bar
        status_bar = QHBoxLayout()
        note_count_str = f"Notes: {len(result.notes)}"
        dur_str = f"Duration: {result.duration:.1f}s"
        tempo_str = f"Tempo: {result.tempo:.1f} BPM"
        dynamics_str = "Dynamics: Recovered" if result.has_velocity else "Dynamics: Synthesized (100)"

        for stat in [note_count_str, dur_str, tempo_str, dynamics_str]:
            lbl = QLabel(stat)
            lbl.setStyleSheet("color: #8e8e98; font-size: 12px; margin-right: 12px;")
            status_bar.addWidget(lbl)

        status_bar.addStretch()
        main_layout.addLayout(status_bar)

        # Playback animation timer
        self._play_timer = QTimer(self)
        self._play_timer.setInterval(33)  # ~30 FPS
        self._play_timer.timeout.connect(self._on_play_tick)

        # Pre-synthesize initial notes in background
        self._rebuild_synth_audio()
        self._load_original_audio()

    def _rebuild_synth_audio(self) -> None:
        """Synthesize active MIDI notes into an audio buffer."""
        self._synth_audio = synthesize_transcription_audio(
            notes=self.result.notes,
            duration=self.piano_roll.total_duration_sec,
            sample_rate=self.sr,
            muted_instruments=self.piano_roll.muted_instruments,
            solo_instruments=self.piano_roll.solo_instruments,
        )

    def _load_original_audio(self) -> None:
        """Load source audio file if present on disk."""
        if self.result.source_audio_path and Path(self.result.source_audio_path).exists():
            try:
                import soundfile as sf
                orig, in_sr = sf.read(self.result.source_audio_path, dtype="float32")
                if orig.ndim == 1:
                    orig = np.column_stack([orig, orig])
                # Ensure length matches total_duration_sec
                target_len = int(self.piano_roll.total_duration_sec * self.sr)
                if in_sr != self.sr:
                    # Quick resample via linear interpolation
                    indices = np.linspace(0, len(orig) - 1, target_len).astype(int)
                    orig = orig[indices]
                if len(orig) < target_len:
                    padded = np.zeros((target_len, 2), dtype=np.float32)
                    padded[:len(orig)] = orig
                    orig = padded
                else:
                    orig = orig[:target_len]
                self._orig_audio = orig
            except Exception as e:
                logger.warning(f"Could not load original audio: {e}")
                self._orig_audio = None
        else:
            self._orig_audio = None

    def get_blended_audio(self) -> np.ndarray:
        """Blend original stem audio and MIDI synth based on blend_slider."""
        if self._synth_audio is None:
            self._rebuild_synth_audio()
        synth = self._synth_audio
        blend = self.blend_slider.value() / 100.0

        if self._orig_audio is not None and len(self._orig_audio) == len(synth):
            return (1.0 - blend) * self._orig_audio + blend * synth
        return synth

    def toggle_play(self) -> None:
        if self._is_playing:
            self.pause_play()
        else:
            self.start_play()

    def start_play(self) -> None:
        import time
        self._is_playing = True
        self.play_btn.setText("⏸ Pause")
        self._play_start_epoch = time.time()
        self._play_offset_sec = self.piano_roll.current_time_sec
        self._play_timer.start()

        # Audio output playback
        try:
            import sounddevice as sd
            blended = self.get_blended_audio()
            start_frame = int(self._play_offset_sec * self.sr)
            if start_frame < len(blended):
                sd.stop()
                sd.play(blended[start_frame:], samplerate=self.sr)
        except Exception as e:
            logger.debug(f"sounddevice playback not available: {e}")

    def pause_play(self) -> None:
        self._is_playing = False
        self.play_btn.setText("▶ Play")
        self._play_timer.stop()
        try:
            import sounddevice as sd
            sd.stop()
        except Exception:
            pass

    def stop_play(self) -> None:
        self.pause_play()
        self.seek_to(0.0)

    def seek_to(self, sec: float) -> None:
        import time
        clamped = max(0.0, min(self.piano_roll.total_duration_sec, sec))
        self.piano_roll.set_current_time(clamped)
        self.time_lbl.setText(f"{clamped:.1f}s / {self.piano_roll.total_duration_sec:.1f}s")
        if self._is_playing:
            self._play_start_epoch = time.time()
            self._play_offset_sec = clamped
            try:
                import sounddevice as sd
                blended = self.get_blended_audio()
                start_frame = int(clamped * self.sr)
                if start_frame < len(blended):
                    sd.stop()
                    sd.play(blended[start_frame:], samplerate=self.sr)
            except Exception:
                pass

    def _on_play_tick(self) -> None:
        import time
        elapsed = time.time() - self._play_start_epoch
        cur_time = self._play_offset_sec + elapsed
        if cur_time >= self.piano_roll.total_duration_sec:
            self.stop_play()
            return
        self.piano_roll.set_current_time(cur_time)
        self.time_lbl.setText(f"{cur_time:.1f}s / {self.piano_roll.total_duration_sec:.1f}s")

    def _on_blend_changed(self, value: int) -> None:
        if self._is_playing:
            # Re-seed playback from current position with updated blend
            self.seek_to(self.piano_roll.current_time_sec)

    def on_mute_toggled(self, instrument: str, is_muted: bool):
        if is_muted:
            self.piano_roll.muted_instruments.add(instrument)
        else:
            self.piano_roll.muted_instruments.discard(instrument)
        self.piano_roll.update()
        self._rebuild_synth_audio()

    def on_solo_toggled(self, instrument: str, is_solo: bool):
        if is_solo:
            self.piano_roll.solo_instruments.add(instrument)
        else:
            self.piano_roll.solo_instruments.discard(instrument)
        self.piano_roll.update()
        self._rebuild_synth_audio()

    def on_export_midi(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Transcription to MIDI", "transcription.mid", "MIDI Files (*.mid)"
        )
        if file_path:
            if self.result.save_midi(file_path):
                QMessageBox.information(self, "Success", f"Saved MIDI to:\n{file_path}")
            else:
                QMessageBox.warning(self, "Error", "Failed to save MIDI file.")

    def closeEvent(self, event):
        self.stop_play()
        super().closeEvent(event)
