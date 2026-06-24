"""
Kraftbeat Block Arranger

A drag-and-drop audio block arranger that lets users import generated
WAV chunks, reorder them visually, and stitch them into a final track
with smooth crossfades. Think of it as a lightweight timeline without
the complexity of a full DAW.
"""

import logging
import os
import time
from pathlib import Path
from typing import List, Optional

import numpy as np

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QFileDialog, QMessageBox,
    QSlider, QSpinBox, QGroupBox, QProgressBar, QFrame,
    QAbstractItemView, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QMimeData
from PyQt6.QtGui import QFont, QIcon, QColor

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------------

class AudioBlock:
    """Represents a single audio block in the arranger."""
    
    def __init__(self, path: str):
        self.path = path
        self.name = Path(path).stem
        self.duration: Optional[float] = None
        self.sample_rate: Optional[int] = None
        self._audio: Optional[np.ndarray] = None
        self._loaded = False

    def load(self) -> bool:
        """Load audio from disk into memory. Returns True on success."""
        try:
            import soundfile as sf
            data, sr = sf.read(self.path, always_2d=False)
            self._audio = data
            self.sample_rate = sr
            self.duration = len(data) / sr
            self._loaded = True
            return True
        except Exception as e:
            logger.error(f"Failed to load block '{self.name}': {e}")
            return False

    @property
    def audio(self) -> Optional[np.ndarray]:
        if not self._loaded:
            self.load()
        return self._audio

    @property
    def loaded(self) -> bool:
        return self._loaded


# ---------------------------------------------------------------------------
# Render Worker
# ---------------------------------------------------------------------------

class RenderWorker(QThread):
    """Stitches all audio blocks together with crossfades."""
    
    progress = pyqtSignal(int)          # 0–100
    finished = pyqtSignal(str)          # output file path
    error = pyqtSignal(str)

    def __init__(self, blocks: List[AudioBlock], output_path: str, crossfade_ms: int = 500):
        super().__init__()
        self.blocks = blocks
        self.output_path = output_path
        self.crossfade_ms = crossfade_ms

    def run(self):
        try:
            import soundfile as sf

            if not self.blocks:
                self.error.emit("No blocks to render.")
                return

            self.progress.emit(5)

            # Load all blocks and determine common sample rate
            loaded = []
            for i, block in enumerate(self.blocks):
                if not block.load():
                    self.error.emit(f"Could not load block: {block.name}")
                    return
                loaded.append(block)
                self.progress.emit(5 + int(40 * (i + 1) / len(self.blocks)))

            # Use the sample rate of the first block as the master
            master_sr = loaded[0].sample_rate
            crossfade_samples = int(master_sr * self.crossfade_ms / 1000)

            self.progress.emit(50)

            result = None

            for i, block in enumerate(loaded):
                audio = block.audio

                # Convert to float32 for mixing
                if audio.dtype != np.float32:
                    audio = audio.astype(np.float32)

                # Resample if needed (basic linear interpolation approach)
                if block.sample_rate != master_sr:
                    try:
                        from scipy.signal import resample_poly
                        from math import gcd
                        g = gcd(master_sr, block.sample_rate)
                        up = master_sr // g
                        down = block.sample_rate // g
                        if audio.ndim == 1:
                            audio = resample_poly(audio, up, down)
                        else:
                            audio = np.stack(
                                [resample_poly(audio[:, c], up, down) for c in range(audio.shape[1])],
                                axis=1
                            )
                    except ImportError:
                        pass  # scipy not available, skip resample

                if result is None:
                    result = audio
                else:
                    # Apply crossfade between result tail and new block head
                    if crossfade_samples > 0 and len(result) > crossfade_samples and len(audio) > crossfade_samples:
                        fade_out = np.linspace(1.0, 0.0, crossfade_samples)
                        fade_in  = np.linspace(0.0, 1.0, crossfade_samples)

                        if result.ndim > 1:
                            fade_out = fade_out[:, np.newaxis]
                            fade_in  = fade_in[:, np.newaxis]

                        # Overlap-add the crossfade zone
                        result[-crossfade_samples:] = (
                            result[-crossfade_samples:] * fade_out +
                            audio[:crossfade_samples]  * fade_in
                        )
                        result = np.concatenate([result, audio[crossfade_samples:]])
                    else:
                        result = np.concatenate([result, audio])

                self.progress.emit(50 + int(45 * (i + 1) / len(loaded)))

            # Normalize to prevent clipping
            peak = np.max(np.abs(result))
            if peak > 0:
                result = result / peak * 0.92

            # Save
            sf.write(self.output_path, result, master_sr)
            self.progress.emit(100)
            self.finished.emit(self.output_path)

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.error.emit(str(e))


# ---------------------------------------------------------------------------
# Block List Item Widget
# ---------------------------------------------------------------------------

class BlockItem(QListWidgetItem):
    """Custom list item representing one audio block."""
    
    def __init__(self, block: AudioBlock):
        super().__init__()
        self.block = block
        self._refresh_text()
        self.setToolTip(block.path)

    def _refresh_text(self):
        dur = f"{self.block.duration:.1f}s" if self.block.duration else "?"
        sr  = f"{self.block.sample_rate}Hz" if self.block.sample_rate else "?"
        self.setText(f"🎵  {self.block.name}   [{dur} · {sr}]")


# ---------------------------------------------------------------------------
# Main Arranger Panel
# ---------------------------------------------------------------------------

class ArrangerPanel(QWidget):
    """Block Arranger — drag-and-drop stitching panel."""

    # Emitted when the render is done and user can play it
    render_ready = pyqtSignal(str)   # output file path

    def __init__(self, parent=None):
        super().__init__(parent)
        self.blocks: List[AudioBlock] = []
        self.render_worker: Optional[RenderWorker] = None
        self._setup_ui()

    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(10)

        # ── Header ────────────────────────────────────────────────────
        header = QHBoxLayout()
        title = QLabel("🎛️ Block Arranger")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #a78bfa;")
        header.addWidget(title)
        header.addStretch()

        subtitle = QLabel("Stack · Reorder · Crossfade · Export")
        subtitle.setStyleSheet("color: #808090; font-style: italic;")
        header.addWidget(subtitle)
        root.addLayout(header)

        # ── Toolbar ───────────────────────────────────────────────────
        toolbar = QHBoxLayout()

        self.import_btn = QPushButton("📂 Import Audio")
        self.import_btn.setToolTip("Import WAV / MP3 / FLAC files")
        self.import_btn.clicked.connect(self._import_files)
        toolbar.addWidget(self.import_btn)

        self.import_outputs_btn = QPushButton("🪄 From Outputs/")
        self.import_outputs_btn.setToolTip("Add all files from the outputs/ folder")
        self.import_outputs_btn.clicked.connect(self._import_from_outputs)
        toolbar.addWidget(self.import_outputs_btn)

        toolbar.addStretch()

        self.move_up_btn = QPushButton("⬆ Up")
        self.move_up_btn.clicked.connect(self._move_up)
        toolbar.addWidget(self.move_up_btn)

        self.move_down_btn = QPushButton("⬇ Down")
        self.move_down_btn.clicked.connect(self._move_down)
        toolbar.addWidget(self.move_down_btn)

        self.remove_btn = QPushButton("🗑 Remove")
        self.remove_btn.setStyleSheet("background: #7f1d1d;")
        self.remove_btn.clicked.connect(self._remove_selected)
        toolbar.addWidget(self.remove_btn)

        self.clear_btn = QPushButton("✕ Clear All")
        self.clear_btn.setStyleSheet("background: #3f3f46;")
        self.clear_btn.clicked.connect(self._clear_all)
        toolbar.addWidget(self.clear_btn)

        root.addLayout(toolbar)

        # ── Block List ────────────────────────────────────────────────
        self.block_list = QListWidget()
        self.block_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.block_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.block_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.block_list.setAlternatingRowColors(True)
        self.block_list.setStyleSheet("""
            QListWidget {
                background: #1a1a22;
                border: 2px solid #3f3f56;
                border-radius: 8px;
                font-size: 13px;
                color: #dddde8;
            }
            QListWidget::item {
                padding: 10px 12px;
                border-bottom: 1px solid #2e2e3e;
            }
            QListWidget::item:selected {
                background: #6d28d9;
                color: white;
            }
            QListWidget::item:hover {
                background: #2e2e45;
            }
            QListWidget::item:alternate {
                background: #1e1e2e;
            }
        """)
        self.block_list.model().rowsMoved.connect(self._sync_blocks_from_list)
        self.block_list.setMinimumHeight(200)
        root.addWidget(self.block_list, stretch=1)

        # ── Empty state label ─────────────────────────────────────────
        self.empty_label = QLabel(
            "⬆  Import audio files above, or click \"From Outputs/\" to load your recently generated tracks.\n\n"
            "Drag rows to reorder · Select and use ⬆ ⬇ buttons to move blocks"
        )
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("color: #55556a; font-size: 13px;")
        root.addWidget(self.empty_label)

        # ── Timeline summary ──────────────────────────────────────────
        self.summary_label = QLabel()
        self.summary_label.setStyleSheet("color: #a0a0b8; font-size: 12px;")
        root.addWidget(self.summary_label)

        # ── Render Settings ───────────────────────────────────────────
        settings_group = QGroupBox("Render Settings")
        settings_layout = QHBoxLayout(settings_group)

        settings_layout.addWidget(QLabel("Crossfade:"))
        from utils.config import get_config
        max_crossfade = get_config("max_crossfade_ms", 5000)
        self.crossfade_spin = QSpinBox()
        self.crossfade_spin.setRange(0, max_crossfade)
        self.crossfade_spin.setValue(500)
        self.crossfade_spin.setSuffix(" ms")
        self.crossfade_spin.setToolTip("Overlap duration between adjacent blocks (0 = hard cut)")
        settings_layout.addWidget(self.crossfade_spin)

        settings_layout.addStretch()

        self.total_label = QLabel("Total: 0 blocks · 0s")
        self.total_label.setStyleSheet("color: #808090;")
        settings_layout.addWidget(self.total_label)

        root.addWidget(settings_group)

        # ── Progress ──────────────────────────────────────────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar::chunk { background: #7c3aed; }")
        root.addWidget(self.progress_bar)

        # ── Render Button ─────────────────────────────────────────────
        render_row = QHBoxLayout()
        render_row.addStretch()

        self.render_btn = QPushButton("🎚️  Render Final Track")
        self.render_btn.setMinimumHeight(44)
        self.render_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:1 #a855f7);
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 28px;
                border-radius: 8px;
            }
            QPushButton:hover { background: #8b5cf6; }
            QPushButton:disabled { background: #3f3f50; color: #606070; }
        """)
        self.render_btn.clicked.connect(self._render)
        render_row.addWidget(self.render_btn)

        root.addLayout(render_row)

        self._update_state()

    # ------------------------------------------------------------------
    # Block Management
    # ------------------------------------------------------------------

    def _import_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Import Audio Blocks", "",
            "Audio Files (*.wav *.mp3 *.flac *.ogg)"
        )
        for path in paths:
            self._add_block(path)

    def _import_from_outputs(self):
        outputs_dir = os.path.join(os.getcwd(), "outputs")
        if not os.path.exists(outputs_dir):
            QMessageBox.information(self, "Empty", "No outputs/ folder found yet.")
            return

        files = sorted(
            [os.path.join(outputs_dir, f) for f in os.listdir(outputs_dir)
             if f.lower().endswith((".wav", ".mp3", ".flac"))],
            key=os.path.getmtime
        )

        if not files:
            QMessageBox.information(self, "Empty", "No audio files found in outputs/.")
            return

        for path in files:
            self._add_block(path)

    def _add_block(self, path: str):
        # Avoid duplicates
        existing = [b.path for b in self.blocks]
        if path in existing:
            return

        block = AudioBlock(path)
        block.load()           # pre-load metadata
        self.blocks.append(block)

        item = BlockItem(block)
        self.block_list.addItem(item)
        self._update_state()

    def _remove_selected(self):
        row = self.block_list.currentRow()
        if row < 0:
            return
        self.block_list.takeItem(row)
        self.blocks.pop(row)
        self._update_state()

    def _clear_all(self):
        if not self.blocks:
            return
        reply = QMessageBox.question(
            self, "Clear All", "Remove all blocks from the arranger?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.block_list.clear()
            self.blocks.clear()
            self._update_state()

    def _move_up(self):
        row = self.block_list.currentRow()
        if row <= 0:
            return
        item = self.block_list.takeItem(row)
        self.blocks.insert(row - 1, self.blocks.pop(row))
        self.block_list.insertItem(row - 1, item)
        self.block_list.setCurrentRow(row - 1)
        self._update_state()

    def _move_down(self):
        row = self.block_list.currentRow()
        if row < 0 or row >= self.block_list.count() - 1:
            return
        item = self.block_list.takeItem(row)
        self.blocks.insert(row + 1, self.blocks.pop(row))
        self.block_list.insertItem(row + 1, item)
        self.block_list.setCurrentRow(row + 1)
        self._update_state()

    def _sync_blocks_from_list(self):
        """Re-sync self.blocks order after an internal drag-drop reorder."""
        new_order = []
        for i in range(self.block_list.count()):
            item = self.block_list.item(i)
            if isinstance(item, BlockItem):
                new_order.append(item.block)
        self.blocks = new_order
        self._update_state()

    # ------------------------------------------------------------------
    # UI State
    # ------------------------------------------------------------------

    def _update_state(self):
        has_blocks = bool(self.blocks)
        self.empty_label.setVisible(not has_blocks)
        self.render_btn.setEnabled(has_blocks)
        self.remove_btn.setEnabled(has_blocks)
        self.clear_btn.setEnabled(has_blocks)
        self.move_up_btn.setEnabled(has_blocks)
        self.move_down_btn.setEnabled(has_blocks)

        if has_blocks:
            total_dur = sum(b.duration or 0 for b in self.blocks)
            mins, secs = divmod(int(total_dur), 60)
            dur_str = f"{mins}m {secs}s" if mins else f"{secs}s"
            self.total_label.setText(
                f"Total: {len(self.blocks)} block{'s' if len(self.blocks)>1 else ''} · {dur_str}"
            )
        else:
            self.total_label.setText("Total: 0 blocks · 0s")

    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------

    def _render(self):
        if not self.blocks:
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Rendered Track", "kraftbeat_arrangement.wav",
            "WAV Files (*.wav)"
        )
        if not path:
            return

        self.render_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.render_worker = RenderWorker(
            blocks=list(self.blocks),
            output_path=path,
            crossfade_ms=self.crossfade_spin.value(),
        )
        self.render_worker.progress.connect(self.progress_bar.setValue)
        self.render_worker.finished.connect(self._on_render_done)
        self.render_worker.error.connect(self._on_render_error)
        self.render_worker.start()

    def _on_render_done(self, path: str):
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)
        self.render_btn.setEnabled(True)
        self.render_ready.emit(path)
        QMessageBox.information(
            self, "Render Complete",
            f"✅ Track rendered successfully!\n\n{path}"
        )

    def _on_render_error(self, msg: str):
        self.progress_bar.setVisible(False)
        self.render_btn.setEnabled(True)
        QMessageBox.critical(self, "Render Failed", f"❌ {msg}")
