"""
DiffRhythm Panel - Fast Long-Form Music Generation

Dedicated UI panel for DiffRhythm music generation which produces
coherent 4m45s songs in approximately 10 seconds.
"""

import logging
from pathlib import Path
from typing import Optional
import numpy as np

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QTextEdit, QPushButton, QSlider, QSpinBox, QDoubleSpinBox,
    QProgressBar, QFrame, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

logger = logging.getLogger(__name__)


class DiffRhythmGenerationWorker(QThread):
    """Background worker for DiffRhythm generation."""
    
    finished = pyqtSignal(object)
    progress = pyqtSignal(int)
    error = pyqtSignal(str)
    status = pyqtSignal(str)
    
    def __init__(self, loader, params: dict):
        super().__init__()
        self.loader = loader
        self.params = params
        
    def run(self):
        try:
            # Check for interruption before starting
            if self.isInterruptionRequested():
                return
                
            self.status.emit("Generating with DiffRhythm...")
            audio = self.loader.generate(**self.params)
            
            if self.isInterruptionRequested():
                return
            
            if audio is not None:
                self.finished.emit(audio)
            else:
                self.error.emit("Generation returned no audio")
        except Exception as e:
            self.error.emit(str(e))


class DiffRhythmPanel(QWidget):
    """DiffRhythm music generation panel - fast long-form generation."""
    
    play_audio = pyqtSignal(object, int)
    
    STYLE_PRESETS = {
        "Select a Style Preset...": "",
        
        # --- VOCAL-FOCUSED (Minimal Backing) ---
        "Vocal - Acapella Solo": "acapella, solo voice, no instruments, pure vocals, clear",
        "Vocal - Acapella Group": "acapella group, vocal harmonies, no instruments, beatbox",
        "Vocal - Minimal Piano": "solo vocals, sparse piano, intimate, ballad style",
        "Vocal - Minimal Guitar": "singer-songwriter, acoustic guitar only, intimate, unplugged",
        "Vocal - Ambient Pad": "ethereal vocals, ambient pad, minimal, atmospheric",
        
        # --- FULL PRODUCTION ---
        "Full - Pop Hit": "full pop production, layered synths, drums, bass, polished, radio-ready",
        "Full - Rock Band": "full band rock, electric guitars, drums, bass, powerful, stadium",
        "Full - EDM Festival": "full EDM, drops, builds, synths, processed vocals, festival",
        "Full - Hip Hop Beat": "full hip hop, 808s, hi-hats, trap beat, vocal processing",
        "Full - Orchestra Epic": "full orchestral, strings, brass, cinematic, epic vocals",
        "Full - R&B Smooth": "full r&b, smooth bass, keys, drums, silky vocals, sensual",
        
        # --- Pop / Mainstream ---
        "Pop - Modern Diva": "modern pop, powerful female vocals, belting, upbeat, 120bpm",
        "Pop - Soft Boy": "acoustic pop, soft male vocals, falsetto, intimate, emotional, guitar",
        "Pop - Retro 80s": "80s pop, nostalgic, gated reverb, dramatic vocals, synthwave",
        "Pop - K-Pop Energy": "k-pop, energetic, catchy hook, harmonized, polished production",
        "Pop - Dreamy": "dream pop, breathy vocals, heavy reverb, ethereal, floating",
        
        # --- Rock / Metal ---
        "Rock - Classic Anthem": "classic rock, powerful male vocals, gritty, stadium anthem",
        "Rock - Emo/Punk": "pop punk, angsty vocals, emotional shouting, high energy, fast",
        "Rock - Grunge": "grunge, rasping male vocals, angst, raw emotion, slurred",
        "Metal - Symphonic": "symphonic metal, operatic female vocals, choir, epic orchestra",
        "Metal - Power": "power metal, soaring high-pitched male vocals, vibrato, epic",
        
        # --- Hip Hop / Rap ---
        "Hip Hop - Trap": "trap, hard 808s, hi-hats, aggressive flow, ad-libs",
        "Hip Hop - Boom Bap": "boom bap, old school, jazz samples, conscious lyrics",
        "Hip Hop - Mumble": "trap, auto-tuned vocals, melodic rap, triplets, ad-libs",
        
        # --- R&B / Soul ---
        "R&B - Soulful": "r&b, melismatic female vocals, runs, soul, smooth, emotional",
        "R&B - Crooner": "neo-soul, smooth male vocals, low register, romantic, falsetto",
        "R&B - 90s Group": "90s r&b, vocal harmonies, new jack swing, call and response",
        
        # --- Electronic / Dance ---
        "EDM - Anthem": "progressive house, uplifting female vocals, soaring chorus, festival",
        "EDM - Trance": "vocal trance, ethereal female vocals, emotional, reverb, arpeggios",
        "EDM - Hyperpop": "hyperpop, pitched-up vocals, glitchy, distorted, chaotic, cute",
        "Electronic - Chill": "chillwave, relaxed vocals, lo-fi beats, ambient, sunset vibes",
        "Electronic - Dark": "dark electronic, industrial, distorted vocals, aggressive, heavy",
        
        # --- Country / Folk ---
        "Country - Modern": "modern country, male vocals, storytelling, acoustic, stadium",
        "Country - Classic": "classic country, twang, pedal steel, honky tonk, heartbreak",
        "Folk - Indie": "indie folk, soft harmonies, acoustic, banjo, intimate, campfire",
        "Folk - Celtic": "celtic folk, ethereal female vocals, grace notes, irish, fiddle",
        
        # --- Jazz / Blues ---
        "Jazz - Smooth": "smooth jazz, saxophone, mellow vocals, sophisticated, night club",
        "Jazz - Swing": "big band swing, scatting, brass section, upbeat, vintage",
        "Blues - Electric": "electric blues, gritty male vocals, B.B. King style, guitar",
        "Blues - Acoustic": "acoustic delta blues, raw, slide guitar, front porch, nostalgic",
        
        # --- World / Ethnic ---
        "Latin - Reggaeton": "reggaeton, dembow rhythm, auto-tuned male, party, spanish",
        "Latin - Bachata": "bachata, romantic, spanish guitar, sensual, latin vocals",
        "African - Afrobeats": "afrobeats, bouncy rhythm, highlife, vocals in pidgin, party",
        "Bollywood - Modern": "bollywood, high-pitched female, energetic, hindi, film music",
        
        # --- Vintage Eras ---
        "Vintage - 50s Doo-Wop": "50s doo-wop, group harmony, shoo-wop, romantic male vocals",
        "Vintage - 60s Motown": "60s motown, soul, backup singers, tambourine, upbeat",
        "Vintage - 70s Disco": "70s disco, falsetto, strings, four on the floor, dancefloor",
        "Vintage - 80s Synth": "80s synth-pop, vocoder, drum machines, nostalgic, neon",
        "Vintage - 90s Grunge": "90s grunge, angst, rasping vocals, loud quiet loud",
        
        # --- Theatrical ---
        "Musical - Broadway": "broadway musical, theatrical, clear diction, orchestral",
        "Musical - Disney": "disney style, princess vocals, soaring ballad, magical",
        "Opera - Soprano": "opera, solo soprano, vibrato, aria, classical accompaniment",
        
        # --- Ambient / Experimental ---
        "Ambient - Soundscape": "ambient soundscape, ethereal pads, minimal vocals, atmospheric",
        "Experimental - Art": "art pop, theatrical, experimental, unique phrasing, avant-garde",
        "Lo-Fi - Chill": "lo-fi hip hop, chill beats, soft vocals, study music, relaxing",
    }

    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.loader = None
        self.worker = None
        self.current_audio = None
        self.sample_rate = 44100
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the DiffRhythm panel UI."""
        # Main layout for the panel (contains scroll area)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll Area
        from PyQt6.QtWidgets import QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Content Widget (holds the actual UI)
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(12)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Title
        title = QLabel("🥁 DiffRhythm - Fast Long-Form Generation")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #66b3ff;")  # Blue theme
        layout.addWidget(title)
        
        subtitle = QLabel("Generate 4m45s songs in ~10 seconds with latent diffusion")
        subtitle.setStyleSheet("color: #808090; margin-bottom: 8px;")
        layout.addWidget(subtitle)
        
        # Main content
        content = QHBoxLayout()
        
        left_panel = self.create_input_panel()
        content.addWidget(left_panel, 1)
        
        right_panel = self.create_output_panel()
        content.addWidget(right_panel, 1)
        
        layout.addLayout(content)
        
        # Progress bar (kept at main level for visibility)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

    
    def create_input_panel(self) -> QWidget:
        """Create the left input panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 8, 0)
        
        # Style/Prompt
        style_group = QGroupBox("Style Prompt")
        style_layout = QVBoxLayout(style_group)
        
        # Presets Combo
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Preset:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(self.STYLE_PRESETS.keys())
        self.preset_combo.currentTextChanged.connect(self.on_preset_changed)
        preset_layout.addWidget(self.preset_combo)
        style_layout.addLayout(preset_layout)
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText(
            "Describe the style, genre, and mood...\n\n"
            "Example: electronic, upbeat, synth bass, energetic drums"
        )
        self.prompt_input.setMaximumHeight(80)
        style_layout.addWidget(self.prompt_input)
        
        layout.addWidget(style_group)
        
        # Lyrics (required for DiffRhythm)
        lyrics_group = QGroupBox("🎤 Lyrics (Required for Vocals)")
        lyrics_group.setStyleSheet("QGroupBox { border-color: #66b3ff; }")
        lyrics_layout = QVBoxLayout(lyrics_group)
        
        self.lyrics_input = QTextEdit()
        self.lyrics_input.setPlaceholderText(
            "DiffRhythm requires lyrics for vocal generation.\n\n"
            "[Verse]\n"
            "Your lyrics here...\n\n"
            "[Chorus]\n"
            "Catchy hook...\n\n"
            "Type '[instrumental]' for no vocals."
        )
        self.lyrics_input.setMinimumHeight(180)
        lyrics_layout.addWidget(self.lyrics_input)
        
        layout.addWidget(lyrics_group)
        layout.addStretch()
        
        return panel
    
    def create_output_panel(self) -> QWidget:
        """Create the right output panel (Simplified)."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 0, 0, 0)
        
        # Info (at top) - styled like ACE-Step
        info_group = QGroupBox("About DiffRhythm")
        info_layout = QVBoxLayout(info_group)
        info_layout.setContentsMargins(8, 4, 8, 4)
        
        info_label = QLabel(
            "<b>DiffRhythm</b> generates complete 4m45s songs with vocals using latent diffusion.<br><br>"
            "<b>Parameters:</b><br>"
            "• <b>Duration:</b> Fixed at 4m45s (285 seconds)<br>"
            "• <b>Seed:</b> For reproducibility (Random = new each time)<br>"
            "• <b>Steps:</b> Diffusion steps (8=fast, 64=best quality)<br>"
            "• <b>CFG:</b> Style adherence (higher = more literal)"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #a0a0b0; font-size: 11px;")
        info_layout.addWidget(info_label)
        layout.addWidget(info_group)
        
        # Model Status (just below Info)
        model_group = QGroupBox("Model Status")
        model_layout = QVBoxLayout(model_group)
        
        self.model_status_label = QLabel("⚪ DiffRhythm not loaded")
        self.model_status_label.setStyleSheet("color: #808090;")
        model_layout.addWidget(self.model_status_label)
        
        self.load_model_btn = QPushButton("Load DiffRhythm Model")
        self.load_model_btn.clicked.connect(self.load_model)
        model_layout.addWidget(self.load_model_btn)
        
        # Install note
        install_note = QLabel(
            "📦 Requires separate installation:\n"
            "git clone https://github.com/ASLP-lab/DiffRhythm"
        )
        install_note.setStyleSheet("color: #606070; font-size: 11px;")
        install_note.setWordWrap(True)
        model_layout.addWidget(install_note)
        
        layout.addWidget(model_group)
        
        # Generate GroupBox
        gen_group = QGroupBox("Generate")
        gen_layout = QVBoxLayout(gen_group)
        gen_layout.setContentsMargins(8, 8, 8, 8)
        
        btn_row = QHBoxLayout()
        self.generate_btn = QPushButton("🥁 Generate Song")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #66b3ff;
                font-size: 13px;
                padding: 8px 16px;
            }
            QPushButton:hover { background-color: #80c3ff; }
            QPushButton:disabled { background-color: #404050; }
        """)
        self.generate_btn.clicked.connect(self.generate)
        btn_row.addWidget(self.generate_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_generation)
        btn_row.addWidget(self.stop_btn)
        
        gen_layout.addLayout(btn_row)
        
        # Status label inside Generate group
        self.status_label = QLabel("Ready - Load DiffRhythm model to begin")
        self.status_label.setStyleSheet("color: #808090; font-size: 11px;")
        gen_layout.addWidget(self.status_label)
        
        layout.addWidget(gen_group)
        
        # Parameters GroupBox - Horizontal layout
        params_group = QGroupBox("Parameters")
        params_layout = QHBoxLayout(params_group)
        params_layout.setContentsMargins(8, 4, 8, 4)
        
        # Duration info
        dur_label = QLabel("⏱ 4m45s")
        dur_label.setStyleSheet("color: #66b3ff; font-weight: bold;")
        dur_label.setToolTip("DiffRhythm generates fixed-length songs (285 seconds)")
        params_layout.addWidget(dur_label)
        
        params_layout.addSpacing(12)
        
        # Seed
        params_layout.addWidget(QLabel("Seed:"))
        self.seed_spin = QSpinBox()
        self.seed_spin.setRange(-1, 999999999)
        self.seed_spin.setValue(-1)
        self.seed_spin.setSpecialValueText("Random")
        params_layout.addWidget(self.seed_spin)
        
        params_layout.addSpacing(12)
        
        # Steps
        params_layout.addWidget(QLabel("Steps:"))
        self.steps_spin = QSpinBox()
        self.steps_spin.setRange(8, 64)
        self.steps_spin.setValue(32)
        self.steps_spin.setToolTip("Diffusion steps (more = better quality, slower)")
        params_layout.addWidget(self.steps_spin)
        
        params_layout.addSpacing(12)
        
        # CFG
        params_layout.addWidget(QLabel("CFG:"))
        self.cfg_slider = QSlider(Qt.Orientation.Horizontal)
        self.cfg_slider.setRange(10, 80)
        self.cfg_slider.setValue(40)
        self.cfg_slider.setFixedWidth(60)
        self.cfg_label = QLabel("4.0")
        self.cfg_slider.valueChanged.connect(
            lambda v: self.cfg_label.setText(f"{v/10:.1f}")
        )
        self.cfg_slider.setToolTip("Classifier-Free Guidance strength")
        params_layout.addWidget(self.cfg_slider)
        params_layout.addWidget(self.cfg_label)
        
        params_layout.addStretch()
        layout.addWidget(params_group)
        
        # Audio stats
        self.audio_info_label = QLabel("")
        self.audio_info_label.setStyleSheet("color: #808090; margin-top: 10px;")
        self.audio_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.audio_info_label)
        
        layout.addStretch()
        
        return panel

    def on_preset_changed(self, preset_name: str):
        """Handle preset selection."""
        if preset_name in self.STYLE_PRESETS:
            prompt = self.STYLE_PRESETS[preset_name]
            if prompt:
                self.prompt_input.setPlainText(prompt)

    def load_model(self):
        """Load DiffRhythm model."""
        self.load_model_btn.setEnabled(False)
        self.status_label.setText("Loading DiffRhythm...")
        self.model_status_label.setText("⏳ Loading...")
        
        self.loader_thread = QThread()
        self.loader_thread.run = self._load_model_thread
        self.loader_thread.finished.connect(self.on_model_loaded)
        self.loader_thread.start()
        
    def _load_model_thread(self):
        try:
            from models.diffrhythm import DiffRhythmLoader
            self.loader = DiffRhythmLoader()
            self.loader.load()
        except Exception as e:
            logger.error(f"Failed to load DiffRhythm: {e}")
            self.loader = None
            
    def on_model_loaded(self):
        if self.loader and self.loader.is_loaded:
            self.model_status_label.setText("🟢 DiffRhythm Loaded")
            self.status_label.setText("Ready to generate!")
            self.load_model_btn.setText("Reload Model")
        else:
            self.model_status_label.setText("🔴 Load Failed")
            self.status_label.setText("Failed to load model. Check console.")
            
        self.load_model_btn.setEnabled(True)

    def generate(self):
        if not self.loader:
            self.load_model()
            return

        prompt = self.prompt_input.toPlainText()
        lyrics = self.lyrics_input.toPlainText()
        
        # Determine duration logic if needed, but DiffRhythm is fixed usually
        # We pass prompt, lyrics, seed
        
        params = {
            "prompt": prompt,
            "lyrics": lyrics,
            "seed": self.seed_spin.value(),
            "steps": self.steps_spin.value(),
            "cfg_strength": self.cfg_slider.value() / 10.0
        }
        
        self.worker = DiffRhythmGenerationWorker(self.loader, params)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.status.connect(lambda s: self.status_label.setText(s))
        
        self.worker.start()
        
        self.generate_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

    def stop_generation(self):
        if self.worker and self.worker.isRunning():
            self.status_label.setText("Stopping...")
            self.worker.requestInterruption()
            # Wait up to 2 seconds for graceful stop
            if not self.worker.wait(2000):
                # Force terminate if still running
                self.worker.terminate()
                self.worker.wait()
            self.status_label.setText("Generation stopped.")
            self.generate_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.progress_bar.setVisible(False)

    
    def on_generation_finished(self, audio):
        self.current_audio = audio
        self.sample_rate = 44100
        
        # Emit callback
        self.play_audio.emit(self.current_audio, self.sample_rate)
        
        duration = audio.shape[-1] / self.sample_rate
        self.audio_info_label.setText(f"✓ Generated: {duration:.1f}s | {self.sample_rate}Hz")
        
        self.generate_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Done! Sent to Global Player.")
    
    def on_generation_error(self, error_msg):
        self.status_label.setText(f"Error: {error_msg}")
        self.generate_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
