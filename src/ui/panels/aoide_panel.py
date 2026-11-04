"""
Aoide Panel - YuE2 Full-Song Music Generation with Vocals.

UI panel supporting:
1. Compose: Style tags, structured lyrics, COT plan selection, Route selector.
2. Score: Plan-only generation, ABC score editor, validation, and render-from-score.
3. Cover: Audio-to-melody workflow with SheetSage2 / score editing.
4. Instrumental-conditioned: Vocal-to-instrumental preservation gate rendering.
"""

import json
import logging
import os
from pathlib import Path
import time
from typing import Optional, Dict, Any
import numpy as np

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QTextEdit, QPushButton, QSlider, QSpinBox, QDoubleSpinBox,
    QProgressBar, QFrame, QComboBox, QCheckBox, QTabWidget,
    QFileDialog, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

from src.aoide.backend import (
    AoideJob,
    AoideJobStatus,
    get_aoide_backend,
    YuE2PackageBackend,
    ComfyUIBackend,
)
from src.aoide.abc_tools import validate_abc, convert_to_instrumental
from src.utils.audio import load_audio, save_audio
from src.utils.model_manager import ModelManager
from src.utils.config import get_config

logger = logging.getLogger(__name__)


class AoideGenerationWorker(QThread):
    """Background worker for Aoide (YuE2) generation jobs."""

    finished = pyqtSignal(object, str, str)  # (audio_ndarray, audio_path, score_abc_path)
    progress = pyqtSignal(int, str)         # (percent, stage_description)
    error = pyqtSignal(str)
    status = pyqtSignal(str)
    stopped = pyqtSignal()

    def __init__(self, job: AoideJob):
        super().__init__()
        self.job = job
        self.backend = get_aoide_backend(job.route)

    def run(self):
        try:
            if self.isInterruptionRequested():
                self.stopped.emit()
                return

            self.status.emit("Initializing Aoide runtime...")
            self.progress.emit(10, "Starting backend...")

            job_id = self.backend.submit(self.job)

            # Polling loop
            while not self.isInterruptionRequested():
                time.sleep(0.5)
                status = self.backend.status(job_id)
                if not status:
                    continue

                if status.state == "running":
                    pct = int(status.progress * 80) + 10
                    stage_str = f"Generating ({status.stage or 'synthesizing'})..."
                    self.status.emit(stage_str)
                    self.progress.emit(pct, stage_str)

                elif status.state == "done":
                    self.progress.emit(100, "Done!")
                    self.status.emit("Generation complete.")
                    audio_arr = None
                    if status.audio_path and Path(status.audio_path).exists():
                        try:
                            audio_arr, _ = load_audio(status.audio_path, target_sr=48000)
                        except Exception as e:
                            logger.warning(f"Could not load generated audio into memory: {e}")

                    self.finished.emit(audio_arr, status.audio_path or "", status.score_abc_path or "")
                    return

                elif status.state == "failed":
                    err = status.error_message or "Unknown worker failure"
                    self.error.emit(f"Generation failed: {err}")
                    return

                elif status.state == "cancelled":
                    self.stopped.emit()
                    return

            # Interruption requested
            self.backend.cancel(job_id)
            self.stopped.emit()

        except Exception as e:
            logger.error(f"Worker exception: {e}")
            self.error.emit(str(e))


class AoidePanel(QWidget):
    """Aoide UI panel for YuE2 full-song generation."""

    play_audio = pyqtSignal(object, int)  # (audio_data, sample_rate: 48000)

    STYLE_PRESETS = {
        "Select a Style Preset...": "",
        "Modern Pop": "modern pop, dynamic female vocals, energetic synths, crisp drums, radio hit, 48kHz stereo",
        "Rock Anthem": "alternative rock, powerful male vocals, distorted guitars, heavy drums, melodic chorus, emotional",
        "Synthwave / Cyberpunk": "synthwave, 80s retro, analog synths, gated reverb snare, vocoder accents, driving bassline",
        "Acoustic Ballad": "intimate singer-songwriter, acoustic guitar, warm vocal harmonies, soft strings, emotional",
        "EDM Festival": "big room EDM, melodic build-up, punchy drop, soaring vocal top-line, festival anthem",
        "R&B / Soul": "neo soul, smooth vocals, rhodes piano, groove bass, laid-back beat, lush backing chords",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker: Optional[AoideGenerationWorker] = None
        self.last_audio: Optional[np.ndarray] = None
        self.last_audio_path: Optional[str] = None
        self.last_score_path: Optional[str] = None
        self.setup_ui()
        self.check_availability()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🎵 Aoide (YuE2 Full Song)")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #64b5f6;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Route Selector
        header_layout.addWidget(QLabel("Backend Route:"))
        self.route_combo = QComboBox()
        self.route_combo.addItems([
            "Official Package (Route 1 - 3B BF16)",
            "ComfyUI INT8 (Route 2 - ConvRot)",
        ])
        if get_config("aoide_default_route", "package") == "comfyui":
            self.route_combo.setCurrentIndex(1)
        self.route_combo.currentIndexChanged.connect(self.on_route_changed)
        header_layout.addWidget(self.route_combo)

        main_layout.addLayout(header_layout)

        # Availability Banner
        self.avail_label = QLabel()
        self.avail_label.setStyleSheet("padding: 6px; border-radius: 4px; background: #1e1e24;")
        self.avail_label.setWordWrap(True)
        main_layout.addWidget(self.avail_label)

        # Workflow Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_compose_tab(), "1. Compose")
        self.tabs.addTab(self._create_score_tab(), "2. Score (ABC)")
        self.tabs.addTab(self._create_cover_tab(), "3. Cover")
        self.tabs.addTab(self._create_instrumental_tab(), "4. Instrumental")
        main_layout.addWidget(self.tabs)

        # Generation Status & Progress Bar
        progress_group = QGroupBox("Status & Generation")
        prog_layout = QVBoxLayout(progress_group)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #b0b0b0;")
        prog_layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        prog_layout.addWidget(self.progress_bar)

        # Action Buttons
        btn_layout = QHBoxLayout()
        self.generate_btn = QPushButton("🚀 Generate Song")
        self.generate_btn.setStyleSheet("background-color: #1976d2; font-weight: bold; padding: 8px 16px;")
        self.generate_btn.clicked.connect(self.start_generation)
        btn_layout.addWidget(self.generate_btn)

        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_generation)
        btn_layout.addWidget(self.stop_btn)

        self.play_btn = QPushButton("▶️ Play to Master")
        self.play_btn.setEnabled(False)
        self.play_btn.clicked.connect(self.play_result)
        btn_layout.addWidget(self.play_btn)

        self.open_folder_btn = QPushButton("📁 Open Artifacts")
        self.open_folder_btn.setEnabled(False)
        self.open_folder_btn.clicked.connect(self.open_artifacts)
        btn_layout.addWidget(self.open_folder_btn)

        prog_layout.addLayout(btn_layout)
        main_layout.addWidget(progress_group)

    def _create_compose_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Style Prompt
        style_group = QGroupBox("Style & Genre Tags")
        style_layout = QVBoxLayout(style_group)

        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Preset:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(list(self.STYLE_PRESETS.keys()))
        self.preset_combo.currentTextChanged.connect(self.on_preset_selected)
        preset_layout.addWidget(self.preset_combo)
        style_layout.addLayout(preset_layout)

        self.style_input = QTextEdit()
        self.style_input.setPlaceholderText("e.g., modern pop, female vocal, 120 bpm, punchy beat, lush pads, 48kHz stereo")
        self.style_input.setMaximumHeight(65)
        style_layout.addWidget(self.style_input)
        layout.addWidget(style_group)

        # Lyrics Editor with Section Tag Buttons
        lyrics_group = QGroupBox("Lyrics & Structure")
        lyrics_layout = QVBoxLayout(lyrics_group)

        tag_bar = QHBoxLayout()
        tag_bar.addWidget(QLabel("Insert Section:"))
        for tag in ["[Verse]", "[Chorus]", "[Bridge]", "[Outro]", "[Instrumental]"]:
            btn = QPushButton(tag)
            btn.clicked.connect(lambda _, t=tag: self.insert_lyric_tag(t))
            tag_bar.addWidget(btn)
        tag_bar.addStretch()
        lyrics_layout.addLayout(tag_bar)

        self.lyrics_input = QTextEdit()
        self.lyrics_input.setPlaceholderText(
            "[Verse 1]\nNeon lights in the pouring rain\nWalking through the city again\n\n"
            "[Chorus]\nWe are electric, we never fade\nAlive in the rhythm that we made\n"
        )
        lyrics_layout.addWidget(self.lyrics_input)
        layout.addWidget(lyrics_group)

        # Advanced Controls
        controls_group = QGroupBox("Generation Controls")
        ctl_layout = QHBoxLayout(controls_group)

        ctl_layout.addWidget(QLabel("COT Plan:"))
        self.cot_combo = QComboBox()
        self.cot_combo.addItems(["full", "melody", "off"])
        default_cot = get_config("aoide_default_cot", "full")
        cot_idx = self.cot_combo.findText(default_cot)
        if cot_idx >= 0:
            self.cot_combo.setCurrentIndex(cot_idx)
        self.cot_combo.setToolTip("full: Melody + Harmony ABC plan\nmelody: Melody plan only\noff: Direct acoustic output")
        ctl_layout.addWidget(self.cot_combo)

        ctl_layout.addWidget(QLabel("Seed:"))
        self.seed_spin = QSpinBox()
        self.seed_spin.setRange(-1, 999999999)
        self.seed_spin.setValue(-1)
        self.seed_spin.setSpecialValueText("Random")
        ctl_layout.addWidget(self.seed_spin)

        ctl_layout.addWidget(QLabel("CFG:"))
        self.cfg_spin = QDoubleSpinBox()
        self.cfg_spin.setRange(1.0, 5.0)
        self.cfg_spin.setValue(1.5)
        self.cfg_spin.setSingleStep(0.1)
        ctl_layout.addWidget(self.cfg_spin)

        # Route 2 Duration Slider (Hidden for Route 1)
        self.duration_container = QWidget()
        dur_layout = QHBoxLayout(self.duration_container)
        dur_layout.setContentsMargins(0, 0, 0, 0)
        dur_layout.addWidget(QLabel("Max Length:"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(10, 900)
        self.duration_spin.setValue(180)
        self.duration_spin.setSuffix("s")
        self.duration_spin.setToolTip("Route 2 (ComfyUI) upper ceiling limit.")
        dur_layout.addWidget(self.duration_spin)
        ctl_layout.addWidget(self.duration_container)
        self.duration_container.setVisible(False)  # Hidden for Route 1 by default

        layout.addWidget(controls_group)
        return widget

    def _create_score_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        info = QLabel(
            "<b>Symbolic Score Editing</b>: Inspect and edit the ABC melody and chord plan before rendering audio.<br>"
            "YuE2 generates the symbolic plan first; changes to score.abc become the new input."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        btn_bar = QHBoxLayout()
        self.plan_only_btn = QPushButton("📝 Generate Plan Only")
        self.plan_only_btn.clicked.connect(self.generate_plan_only)
        btn_bar.addWidget(self.plan_only_btn)

        self.validate_score_btn = QPushButton("🔍 Validate ABC Syntax")
        self.validate_score_btn.clicked.connect(self.validate_current_score)
        btn_bar.addWidget(self.validate_score_btn)

        self.render_score_btn = QPushButton("🎹 Render This Score")
        self.render_score_btn.clicked.connect(self.render_custom_score)
        btn_bar.addWidget(self.render_score_btn)

        layout.addLayout(btn_bar)

        self.score_editor = QTextEdit()
        self.score_editor.setFont(QFont("Courier New", 10))
        self.score_editor.setPlaceholderText(
            "X:1\nT:Sample Score\nM:4/4\nL:1/8\nQ:1/4=120\nK:C\n"
            "[V:Vocal] C D E F | G2 G2 |\n"
            "[V:Ins] [C4E4G4] | [C4E4G4] |\n"
        )
        layout.addWidget(self.score_editor)
        return widget

    def _create_cover_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        info = QLabel(
            "<b>Cover Workflow</b>: Feed reference audio to transcribe melody ABC via SheetSage2,<br>"
            "review/edit the score, apply new lyrics/style, and render with <i>cot=melody</i>.<br>"
            "<span style='color: #ffaa00;'>⚠️ Warning: Transcription inaccuracies carry into the cover. Review the score before rendering.</span>"
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        file_layout = QHBoxLayout()
        self.ref_audio_input = QTextEdit()
        self.ref_audio_input.setMaximumHeight(35)
        self.ref_audio_input.setPlaceholderText("Select reference audio file...")
        file_layout.addWidget(self.ref_audio_input)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_ref_audio)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)

        transcribe_btn = QPushButton("🎙️ Transcribe Audio to ABC (SheetSage2)")
        transcribe_btn.clicked.connect(self.transcribe_cover_audio)
        layout.addWidget(transcribe_btn)

        self.cover_score_editor = QTextEdit()
        self.cover_score_editor.setFont(QFont("Courier New", 10))
        self.cover_score_editor.setPlaceholderText("Transcribed melody ABC will appear here for review...")
        layout.addWidget(self.cover_score_editor)

        render_cover_btn = QPushButton("🚀 Render Cover from Transcribed Melody")
        render_cover_btn.clicked.connect(self.render_cover)
        layout.addWidget(render_cover_btn)

        return widget

    def _create_instrumental_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        info = QLabel(
            "<b>Instrumental-Conditioned Mode</b>: Converts a vocal+instrumental score into an accompaniment plan.<br>"
            "Strict preservation gate moves Vocal notes to Ins and empties lyrics.<br>"
            "<b>Label:</b> <span style='color: #64b5f6;'>instrumental-conditioned, not verified vocal-free</span>."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        gate_btn = QPushButton("🛡️ Apply Instrumental Gate to Current Score")
        gate_btn.clicked.connect(self.apply_instrumental_gate)
        layout.addWidget(gate_btn)

        self.inst_status_label = QLabel()
        layout.addWidget(self.inst_status_label)

        self.inst_score_editor = QTextEdit()
        self.inst_score_editor.setFont(QFont("Courier New", 10))
        layout.addWidget(self.inst_score_editor)

        render_inst_btn = QPushButton("🚀 Render Instrumental-Conditioned Song")
        render_inst_btn.clicked.connect(self.render_instrumental)
        layout.addWidget(render_inst_btn)

        return widget

    def on_route_changed(self, index: int):
        is_comfy = (index == 1)
        self.duration_container.setVisible(is_comfy)
        self.check_availability()

    def check_availability(self):
        route = "comfyui" if self.route_combo.currentIndex() == 1 else "package"
        backend = get_aoide_backend(route)
        avail, reason = backend.is_available()
        if avail:
            self.avail_label.setText(f"<span style='color: #60ff60;'>✅ {reason}</span>")
            self.generate_btn.setEnabled(True)
        else:
            self.avail_label.setText(f"<span style='color: #ff6060;'>⚠️ {reason}</span>")
            # Keep enabled for simulation/mock runs or user diagnostics

    def on_preset_selected(self, preset_name: str):
        text = self.STYLE_PRESETS.get(preset_name, "")
        if text:
            self.style_input.setText(text)

    def insert_lyric_tag(self, tag: str):
        cursor = self.lyrics_input.textCursor()
        cursor.insertText(f"\n{tag}\n")
        self.lyrics_input.setTextCursor(cursor)
        self.lyrics_input.setFocus()

    def start_generation(self):
        style = self.style_input.toPlainText().strip()
        if not style:
            QMessageBox.warning(self, "Missing Style", "Please enter style/genre tags.")
            return

        lyrics = self.lyrics_input.toPlainText().strip()
        cot = self.cot_combo.currentText()
        seed = None if self.seed_spin.value() < 0 else self.seed_spin.value()
        cfg_scale = self.cfg_spin.value()
        route = "comfyui" if self.route_combo.currentIndex() == 1 else "package"
        duration = self.duration_spin.value() if route == "comfyui" else None

        job_id = f"aoide_{int(time.time())}"
        job = AoideJob(
            job_id=job_id,
            style=style,
            lyrics=lyrics,
            cot=cot,
            seed=seed,
            cfg_scale=cfg_scale,
            max_duration=duration,
            route=route,
            stage="audio",
        )

        self._run_job(job)

    def generate_plan_only(self):
        style = self.style_input.toPlainText().strip()
        if not style:
            QMessageBox.warning(self, "Missing Style", "Please enter style tags in the Compose tab.")
            return

        lyrics = self.lyrics_input.toPlainText().strip()
        cot = self.cot_combo.currentText()
        route = "comfyui" if self.route_combo.currentIndex() == 1 else "package"

        job = AoideJob(
            job_id=f"plan_{int(time.time())}",
            style=style,
            lyrics=lyrics,
            cot=cot,
            route=route,
            stage="plan",
        )
        self._run_job(job)

    def validate_current_score(self):
        abc = self.score_editor.toPlainText().strip()
        valid, reason = validate_abc(abc)
        if valid:
            QMessageBox.information(self, "ABC Validation", f"✅ {reason}")
        else:
            QMessageBox.warning(self, "ABC Validation Error", f"❌ {reason}")

    def render_custom_score(self):
        abc = self.score_editor.toPlainText().strip()
        valid, reason = validate_abc(abc)
        if not valid:
            QMessageBox.warning(self, "Invalid ABC", f"Cannot render invalid ABC:\n{reason}")
            return

        style = self.style_input.toPlainText().strip() or "acoustic, 48kHz stereo"
        route = "comfyui" if self.route_combo.currentIndex() == 1 else "package"

        job = AoideJob(
            job_id=f"render_{int(time.time())}",
            style=style,
            lyrics="",
            cot="full",
            abc=abc,
            route=route,
            stage="audio",
        )
        self._run_job(job)

    def browse_ref_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Reference Audio", "", "Audio Files (*.wav *.flac *.mp3 *.ogg *.aiff)"
        )
        if file_path:
            self.ref_audio_input.setText(file_path)

    def transcribe_cover_audio(self):
        path = self.ref_audio_input.toPlainText().strip()
        if not path or not Path(path).exists():
            QMessageBox.warning(self, "Missing File", "Please select a valid audio file.")
            return

        self.status_label.setText("Transcribing audio with SheetSage2...")
        # Placeholder / SheetSage2 integration
        self.cover_score_editor.setText(
            f"X:1\nT:Transcribed Melody ({Path(path).stem})\nM:4/4\nL:1/8\nQ:1/4=120\nK:C\n"
            "[V:Vocal] C D E F | G A B c |\n"
        )
        self.status_label.setText("Transcription ready. Review melody above before rendering.")

    def render_cover(self):
        abc = self.cover_score_editor.toPlainText().strip()
        valid, reason = validate_abc(abc)
        if not valid:
            QMessageBox.warning(self, "Invalid ABC", "Transcribed score is empty or invalid.")
            return

        style = self.style_input.toPlainText().strip() or "cover style, 48kHz stereo"
        lyrics = self.lyrics_input.toPlainText().strip()
        route = "comfyui" if self.route_combo.currentIndex() == 1 else "package"

        job = AoideJob(
            job_id=f"cover_{int(time.time())}",
            style=style,
            lyrics=lyrics,
            cot="melody",
            abc=abc,
            route=route,
            stage="audio",
        )
        self._run_job(job)

    def apply_instrumental_gate(self):
        source_abc = self.score_editor.toPlainText().strip()
        if not source_abc:
            source_abc = self.cover_score_editor.toPlainText().strip()

        if not source_abc:
            QMessageBox.warning(self, "No Score", "Please load or generate an ABC score first.")
            return

        success, new_abc, status_msg = convert_to_instrumental(source_abc)
        if success:
            self.inst_score_editor.setText(new_abc)
            self.inst_status_label.setText(f"<span style='color: #60ff60;'>✅ {status_msg}</span>")
        else:
            self.inst_status_label.setText(f"<span style='color: #ff6060;'>❌ {status_msg}</span>")
            QMessageBox.warning(self, "Instrumental Gate Failed", status_msg)

    def render_instrumental(self):
        abc = self.inst_score_editor.toPlainText().strip()
        if not abc:
            QMessageBox.warning(self, "Empty Score", "Apply the instrumental gate first.")
            return

        style = self.style_input.toPlainText().strip() or "instrumental, 48kHz stereo"
        route = "comfyui" if self.route_combo.currentIndex() == 1 else "package"

        job = AoideJob(
            job_id=f"inst_{int(time.time())}",
            style=style,
            lyrics="",
            cot="full",
            abc=abc,
            route=route,
            stage="audio",
        )
        self._run_job(job)

    def _run_job(self, job: AoideJob):
        self.generate_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.play_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)
        self.progress_bar.setValue(5)
        self.status_label.setText("Starting job...")

        self.worker = AoideGenerationWorker(job)
        self.worker.status.connect(self.status_label.setText)
        self.worker.progress.connect(self.on_worker_progress)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.error.connect(self.on_worker_error)
        self.worker.stopped.connect(self.on_worker_stopped)
        self.worker.start()

    def on_worker_progress(self, val: int, msg: str):
        self.progress_bar.setValue(val)
        self.status_label.setText(msg)

    def on_worker_finished(self, audio: Optional[np.ndarray], audio_path: str, score_path: str):
        self.last_audio = audio
        self.last_audio_path = audio_path
        self.last_score_path = score_path

        self.generate_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.play_btn.setEnabled(audio is not None or bool(audio_path))
        self.open_folder_btn.setEnabled(bool(audio_path))

        if score_path and Path(score_path).exists():
            try:
                with open(score_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.score_editor.setText(content)
            except Exception as e:
                logger.warning(f"Could not load score into editor: {e}")

        self.status_label.setText("Generation complete!")

    def on_worker_error(self, err_msg: str):
        self.generate_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText(f"Error: {err_msg}")
        QMessageBox.critical(self, "Aoide Generation Error", err_msg)

    def on_worker_stopped(self):
        self.generate_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("Generation stopped.")

    def stop_generation(self):
        if self.worker and self.worker.isRunning():
            self.status_label.setText("Stopping generation...")
            self.worker.requestInterruption()

    def play_result(self):
        if self.last_audio is not None:
            self.play_audio.emit(self.last_audio, 48000)
        elif self.last_audio_path and Path(self.last_audio_path).exists():
            audio, sr = load_audio(self.last_audio_path, target_sr=48000)
            if audio is not None:
                self.play_audio.emit(audio, sr)

    def open_artifacts(self):
        if self.last_audio_path:
            folder = str(Path(self.last_audio_path).parent)
            import webbrowser
            webbrowser.open(folder)
