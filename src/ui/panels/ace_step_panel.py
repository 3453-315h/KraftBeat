"""
ACE-Step Panel - AI Music Generation with Vocals

Dedicated UI panel for ACE-Step music generation which supports
lyrics-aware vocal generation.
"""

import logging
from pathlib import Path
from typing import Optional
import numpy as np

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QTextEdit, QPushButton, QSlider, QSpinBox, QDoubleSpinBox,
    QProgressBar, QFrame, QComboBox, QCheckBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

logger = logging.getLogger(__name__)


class ACEStepGenerationWorker(QThread):
    """Background worker for ACE-Step generation."""
    
    finished = pyqtSignal(object)  # numpy array or None
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
                
            self.status.emit("Preparing generation...")
            
            # Validate reference audio file exists if provided
            # Note: ACE-Step pipeline loads audio from path internally
            ref_audio_path = self.params.get('ref_audio_path', '')
            if ref_audio_path and self.params.get('audio2audio_enable', False):
                import os
                if not os.path.exists(ref_audio_path):
                    logger.warning(f"Reference audio not found: {ref_audio_path}")
                    self.params['audio2audio_enable'] = False
                else:
                    logger.info(f"Audio2Audio enabled with: {ref_audio_path}")
            
            # Check for interruption again
            if self.isInterruptionRequested():
                return
                
            self.status.emit("Generating with ACE-Step...")
            logger.info("Worker: Starting generation...")
            audio = self.loader.generate(**self.params)
            
            if self.isInterruptionRequested():
                return
            
            if audio is not None:
                logger.info(f"Worker: Generation successful! Audio shape: {audio.shape}")
                self.finished.emit(audio)
            else:
                logger.error("Worker: Generation returned None!")
                self.error.emit("Generation returned no audio")
        except Exception as e:
            logger.error(f"Worker: Exception during generation: {e}")
            import traceback
            traceback.print_exc()
            self.error.emit(str(e))


class ACEStepPanel(QWidget):
    """ACE-Step music generation panel with lyrics support."""
    
    # Signal to request audio playback from main window
    play_audio = pyqtSignal(object, int)  # (audio_data, sample_rate)

    STYLE_PRESETS = {
        "Select a Style Preset...": "",
        
        # --- VOCAL-FOCUSED (Minimal Backing) ---
        "Vocal - Acapella Solo": "acapella, solo voice, no instruments, pure vocals, clear recording",
        "Vocal - Acapella Group": "acapella group, vocal harmonies, no instruments, beatbox rhythm",
        "Vocal - Minimal Piano": "solo vocals, sparse piano accompaniment, intimate, ballad style",
        "Vocal - Minimal Guitar": "singer-songwriter, acoustic guitar only, intimate vocals, unplugged",
        "Vocal - Ambient Pad": "ethereal vocals, ambient pad background, minimal, atmospheric, spacious",
        "Vocal - Spoken Word": "spoken word, poetry reading, ambient drone, focus on voice, clear diction",
        
        # --- FULL PRODUCTION (Rich Instrumentation) ---
        "Full - Pop Hit": "full pop production, layered synths, drums, bass, polished vocals, radio-ready",
        "Full - Rock Band": "full band rock, electric guitars, drums, bass, powerful vocals, stadium",
        "Full - EDM Festival": "full EDM production, drops, builds, synths, processed vocals, festival",
        "Full - Hip Hop Beat": "full hip hop production, 808s, hi-hats, trap beat, vocal processing",
        "Full - Orchestra Epic": "full orchestral arrangement, strings, brass, cinematic, epic vocals",
        "Full - R&B Smooth": "full r&b production, smooth bass, keys, drums, silky vocals, sensual",
        
        # --- Pop / Mainstream Vocals ---
        "Pop - Modern Diva": "modern pop, upbeat, powerful female vocals, belting, ad-libs, 120bpm",
        "Pop - Soft Boy": "acoustic pop, soft male vocals, falsetto, intimate, emotional, guitar",
        "Pop - Retro 80s": "80s pop, nostalgic, gated reverb, dramatic vocals, synthwave",
        "Pop - K-Pop Girl Group": "k-pop, energetic, female group vocals, harmonized, catchy hook",
        "Pop - K-Pop Boy Band": "k-pop, dynamic male vocals, rap sections, polished production",
        "Pop - Dreamy": "dream pop, breathy female vocals, heavy reverb, ethereal, floating",
        "Pop - Art": "art pop, theatrical vocals, expressive, experimental, unique phrasing",
        
        # --- Rock / Metal Vocals ---
        "Rock - Classic Anthem": "classic rock, powerful male vocals, gritty, stadium anthem",
        "Rock - Emo/Punk": "pop punk, angsty vocals, emotional shouting, high energy, fast",
        "Rock - Grunge": "grunge, rasping male vocals, angst, raw emotion, slurred delivery",
        "Metal - Symphonic": "symphonic metal, operatic female vocals, choir backing, epic",
        "Metal - Deathcore": "deathcore, guttural growls, pig squeals, aggression, heavy",
        "Metal - Power": "power metal, soaring high-pitched male vocals, vibrato, epic storytelling",
        "Rock - Shoegaze": "shoegaze, buried vocals, whispering, dreamy, wall of sound",
        
        # --- Urban / R&B Vocals ---
        "Hip Hop - Lyrical": "hip hop, clear male vocals, rhythmic flow, storytelling, boom bap",
        "Hip Hop - Mumble": "trap, auto-tuned vocals, melodic rap, triplets, ad-libs",
        "Hip Hop - Aggressive": "drill, shouting vocals, aggression, fast flow, dark",
        "R&B - Soulful": "r&b, melismatic female vocals, runs, soul, smooth, emotional",
        "R&B - Crooner": "neo-soul, smooth male vocals, low register, romantic, falsetto",
        "R&B - 90s Group": "90s r&b, vocal harmonies, new jack swing, call and response",
        
        # --- Electronic / Dance Vocals ---
        "EDM - Anthem": "progressive house, uplifting female vocals, soaring chorus, festival",
        "EDM - Trance": "vocal trance, ethereal female vocals, emotional, reverb, arpeggios",
        "EDM - Hyperpop": "hyperpop, pitched-up vocals, glitchy, distorted, chaotic, cute",
        "Electronic - Trip Hop": "trip hop, sultry female vocals, downtempo, dark, moody",
        "Electronic - Vocoder": "daft punk style, robots, vocoder vocals, funk, disco",
        
        # --- Theatrical / Storytelling ---
        "Musical - Broadway": "broadway musical, theatrical projection, clear diction, story-telling, orchestral",
        "Musical - Disney": "disney style, princess vocals, soaring ballad, magical, orchestral",
        "Musical - Villain": "villain song, dark, dramatic, baritone vocals, evil, suspense",
        "Vocal - Spoken Word": "spoken word, poetry reading, clear voice, ambient backing",
        "Vocal - Narration": "documentary narration, deep male voice, serious, cinematic",
        
        # --- Vintage / Eras ---
        "Vintage - 50s Doo-Wop": "50s doo-wop, group harmony, shoo-wop, romantic male vocals",
        "Vintage - 60s Psych": "60s psychedelic rock, reverb heavy vocals, dreamy, beatles style",
        "Vintage - 70s Soul": "70s soul, warm male vocals, wah guitar, funk groove, motown",
        "Vintage - 90s Grunge": "90s grunge, angst, rasping male vocals, loud quiet loud",
        "Vintage - 2000s Pop Punk": "2000s pop punk, nasal male vocals, high energy, fast tempo",
        
        # --- Character / Novelty ---
        "Character - Cartoon": "cartoon voice, high pitched, silly, exaggerated, expressive",
        "Character - Announcer": "stadium announcer, booming voice, echo, energetic",
        "Character - News Anchor": "news anchor, serious tone, clear diction, neutral American accent",
        "Character - Robot": "sci-fi robot, monotonic, metallic, glitchy, futuristic",
        "Character - Whisper": "asmr, whispering, spinetingling, close microphone, intimate",
        
        # --- Traditional / Global Vocals ---
        "Opera - Soprano": "opera, solo soprano, vibrato, aria, classical accompaniment",
        "Opera - Tenor": "opera, solo tenor, powerful, italian style, classical",
        "Choir - Gregorian": "gregorian chant, male choir, monophonic, sacred, reverb",
        "Choir - Gospel": "gospel choir, soulful, clapping, harmonies, uplifting, powerful",
        "Folk - Celtic": "celtic folk, ethereal female vocals, grace notes, irish, fiddle",
        "Latin - Reggaeton": "reggaeton, auto-tuned male vocals, party vibe, spanish",
        "Asian - Bollywood": "bollywood, high-pitched female vocals, energetic, hindi",
        "Asian - Enka": "enka, japanese, kobushi vibrato, emotional, sentimental",
        "Country - Twang": "country, southern accent, male vocals, storytelling, acoustic",
        
        # --- World / Folk (Expanded) ---
        "World - Throat Singing": "tuvan throat singing, deep harmonics, drone, mystical",
        "World - Yodel": "alpine yodeling, rapid pitch change, folk, mountain",
        "World - Fado": "portuguese fado, melancholic female vocals, acoustic guitar, longing",
        "World - Slavic Folk": "slavic folk, female group singing, open throat, bright, piercing",
        "World - Bossa Nova": "bossa nova, soft portuguese vocals, whispery, relaxed",
        
        # --- Texture / FX ---
        "FX - Telephone": "telephone filter, lo-fi, mid-range, distant, radio effect",
        "FX - Megaphone": "megaphone, distorted, public address, shouting, lo-fi",
        "FX - Heavy Autotune": "heavy t-pain effect, hard tuning, robotic pitch, trap",
        "FX - Ethereal Reverb": "massive reverb, church, holy, distant, angelic",
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.loader = None
        self.worker = None
        self.current_audio = None
        self.sample_rate = 44100  # ACE-Step default
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the ACE-Step panel UI."""
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
        title = QLabel("🎤 ACE-Step - Full Song Generation")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #ff7066;")  # Distinctive color
        layout.addWidget(title)
        
        subtitle = QLabel("Generate complete songs with vocals, instruments, and lyrics")
        subtitle.setStyleSheet("color: #808090; margin-bottom: 8px;")
        layout.addWidget(subtitle)
        
        # Main content in horizontal layout
        content = QHBoxLayout()
        
        # Left side - Inputs (more space)
        left_panel = self.create_input_panel()
        content.addWidget(left_panel, 2)
        
        # Right side - Output (compact)
        right_panel = self.create_output_panel()
        content.addWidget(right_panel, 1)
        
        layout.addLayout(content)
        
        # Parameters Group - Full width at bottom
        params_group = QGroupBox("Parameters")
        params_layout = QHBoxLayout(params_group)  # Horizontal for compact full-width layout
        params_layout.setContentsMargins(8, 4, 8, 4)
        
        # Duration
        params_layout.addWidget(QLabel("Duration:"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(10, 240)
        self.duration_spin.setValue(120)
        self.duration_spin.setSuffix("s")
        self.duration_spin.setToolTip("ACE-Step supports up to 240 seconds (4 minutes)")
        params_layout.addWidget(self.duration_spin)
        
        params_layout.addSpacing(16)
        
        # Guidance Scale
        params_layout.addWidget(QLabel("Guidance:"))
        self.guidance_slider = QSlider(Qt.Orientation.Horizontal)
        self.guidance_slider.setRange(10, 150)
        self.guidance_slider.setValue(70)
        self.guidance_slider.setFixedWidth(80)
        self.guidance_label = QLabel("7.0")
        self.guidance_slider.valueChanged.connect(
            lambda v: self.guidance_label.setText(f"{v/10:.1f}")
        )
        params_layout.addWidget(self.guidance_slider)
        params_layout.addWidget(self.guidance_label)
        
        params_layout.addSpacing(16)
        
        # Lyric Guidance
        params_layout.addWidget(QLabel("Lyric:"))
        self.lyric_guidance_slider = QSlider(Qt.Orientation.Horizontal)
        self.lyric_guidance_slider.setRange(10, 50)
        self.lyric_guidance_slider.setValue(20)
        self.lyric_guidance_slider.setFixedWidth(80)
        self.lyric_guidance_label = QLabel("2.0")
        self.lyric_guidance_slider.valueChanged.connect(
            lambda v: self.lyric_guidance_label.setText(f"{v/10:.1f}")
        )
        params_layout.addWidget(self.lyric_guidance_slider)
        params_layout.addWidget(self.lyric_guidance_label)
        
        params_layout.addSpacing(16)
        
        # Inference Steps
        params_layout.addWidget(QLabel("Steps:"))
        self.steps_spin = QSpinBox()
        self.steps_spin.setRange(20, 100)
        self.steps_spin.setValue(60)
        self.steps_spin.setToolTip("More steps = better quality but slower")
        params_layout.addWidget(self.steps_spin)
        
        params_layout.addSpacing(16)
        
        # Seed
        params_layout.addWidget(QLabel("Seed:"))
        self.seed_spin = QSpinBox()
        self.seed_spin.setRange(-1, 999999999)
        self.seed_spin.setValue(-1)
        self.seed_spin.setSpecialValueText("Random")
        self.seed_spin.setToolTip("-1 for random seed")
        params_layout.addWidget(self.seed_spin)
        
        params_layout.addStretch()
        layout.addWidget(params_group)
        
        # Audio Reference (Audio2Audio) Group
        ref_group = QGroupBox("Audio Reference (Optional)")
        ref_layout = QHBoxLayout(ref_group)
        ref_layout.setContentsMargins(8, 4, 8, 4)
        
        self.audio2audio_enable = QCheckBox("Enable")
        self.audio2audio_enable.setToolTip("Use a reference audio to guide the generation style")
        ref_layout.addWidget(self.audio2audio_enable)
        
        self.ref_audio_path = ""
        self.ref_audio_combo = QComboBox()
        self.ref_audio_combo.setMinimumWidth(150)
        self.refresh_voices_list()
        self.ref_audio_combo.currentIndexChanged.connect(self.on_voice_selected)
        ref_layout.addWidget(self.ref_audio_combo)
        
        self.ref_audio_btn = QPushButton("Browse...")
        self.ref_audio_btn.setFixedWidth(80)
        self.ref_audio_btn.clicked.connect(self.browse_ref_audio)
        ref_layout.addWidget(self.ref_audio_btn)
        
        ref_layout.addSpacing(16)
        
        ref_layout.addWidget(QLabel("Strength:"))
        self.ref_strength_slider = QSlider(Qt.Orientation.Horizontal)
        self.ref_strength_slider.setRange(0, 100)
        self.ref_strength_slider.setValue(50)
        self.ref_strength_slider.setFixedWidth(80)
        self.ref_strength_label = QLabel("50%")
        self.ref_strength_slider.valueChanged.connect(
            lambda v: self.ref_strength_label.setText(f"{v}%")
        )
        ref_layout.addWidget(self.ref_strength_slider)
        ref_layout.addWidget(self.ref_strength_label)
        
        ref_layout.addStretch()
        layout.addWidget(ref_group)
        
        # Progress bar (kept at bottom of main panel for visibility)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
    
    def create_input_panel(self) -> QWidget:
        """Create the left input panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 8, 0)
        
        # Style/Prompt Group
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
            "Example: pop, upbeat, female vocals, synth, 120bpm"
        )
        self.prompt_input.setMaximumHeight(80)
        style_layout.addWidget(self.prompt_input)
        
        layout.addWidget(style_group)
        
        # Lyrics Group (ACE-Step specialty!)
        lyrics_group = QGroupBox("🎤 Lyrics (ACE-Step Specialty)")
        lyrics_group.setStyleSheet("QGroupBox { border-color: #ff7066; }")
        lyrics_layout = QVBoxLayout(lyrics_group)
        
        self.lyrics_input = QTextEdit()
        self.lyrics_input.setPlaceholderText(
            "Enter your lyrics here...\n\n"
            "[Verse 1]\n"
            "Walking down the street at night\n"
            "Stars are shining ever bright\n\n"
            "[Chorus]\n"
            "This is my song, my heart's desire\n"
            "Rising higher, like a fire\n\n"
            "Leave empty for instrumental."
        )
        self.lyrics_input.setMinimumHeight(200)
        lyrics_layout.addWidget(self.lyrics_input)
        
        layout.addWidget(lyrics_group)
        
        
        return panel
    
    def create_output_panel(self) -> QWidget:
        """Create the right output panel (Simplified)."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 0, 0, 0)
        
        # Instructions / Info (at top)
        info_group = QGroupBox("About ACE-Step")
        info_layout = QVBoxLayout(info_group)
        info_layout.setContentsMargins(8, 4, 8, 4)
        
        info_label = QLabel(
            "<b>ACE-Step</b> generates full songs with AI vocals from text prompts and lyrics.<br><br>"
            "<b>Parameters:</b><br>"
            "• <b>Duration:</b> Length of audio (10-240 seconds)<br>"
            "• <b>Guidance:</b> Style adherence (higher = more literal)<br>"
            "• <b>Lyric Guidance:</b> Lyrics timing (higher = stricter)<br>"
            "• <b>Steps:</b> Quality vs speed (20=fast, 100=best)<br>"
            "• <b>Seed:</b> For reproducibility (Random = new each time)"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #a0a0b0; font-size: 11px;")
        info_layout.addWidget(info_label)
        
        layout.addWidget(info_group)
        
        # Model Status (with border, compact)
        model_group = QGroupBox("Model Status")
        model_layout = QVBoxLayout(model_group)
        model_layout.setContentsMargins(8, 4, 8, 4)
        model_layout.setSpacing(4)
        
        self.model_status_label = QLabel("⚪ ACE-Step not loaded")
        self.model_status_label.setStyleSheet("color: #808090;")
        model_layout.addWidget(self.model_status_label)
        
        self.load_model_btn = QPushButton("Load ACE-Step Model")
        self.load_model_btn.clicked.connect(self.load_model)
        model_layout.addWidget(self.load_model_btn)
        
        layout.addWidget(model_group)
        
        # Generate controls (in GroupBox under Model Status)
        gen_group = QGroupBox("Generate")
        gen_layout = QVBoxLayout(gen_group)
        gen_layout.setContentsMargins(8, 4, 8, 4)
        gen_layout.setSpacing(4)
        
        btn_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("🎤 Generate with Vocals")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff7066;
                font-size: 13px;
                padding: 8px 16px;
            }
            QPushButton:hover { background-color: #ff8a82; }
            QPushButton:disabled { background-color: #404050; }
        """)
        self.generate_btn.clicked.connect(self.generate)
        btn_layout.addWidget(self.generate_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_generation)
        btn_layout.addWidget(self.stop_btn)
        
        gen_layout.addLayout(btn_layout)
        
        self.status_label = QLabel("Ready - Load ACE-Step model to begin")
        self.status_label.setStyleSheet("color: #808090;")
        gen_layout.addWidget(self.status_label)
        
        layout.addWidget(gen_group)
        
        # Audio stats
        self.audio_info_label = QLabel("")
        self.audio_info_label.setStyleSheet("color: #808090; margin-top: 10px;")
        self.audio_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.audio_info_label)
        
        return panel

    def load_model(self):
        """Load the ACE-Step model."""
        self.load_model_btn.setEnabled(False)
        self.status_label.setText("Loading ACE-Step model...")
        self.model_status_label.setText("⏳ Loading...")
        
        # Import here to avoid circular dependencies if any
        try:
            from models.ace_step import ACEStepLoader
            
            # Use worker for loading to avoid freezing UI
            # For now, simplistic approach or check if ModelLoadWorker is available
            # Let's do direct load in a thread to keep it simple and robust for this fix
            
            self.loader_thread = QThread()
            self.loader_thread.run = self._load_model_thread
            self.loader_thread.finished.connect(self.on_model_loaded)
            self.loader_thread.start()
            
        except Exception as e:
            self.status_label.setText(f"Error loading module: {e}")
            self.load_model_btn.setEnabled(True)

    def _load_model_thread(self):
        """Threaded model loading."""
        try:
            from models.ace_step import ACEStepLoader
            self.loader = ACEStepLoader()
            self.loader.load()
        except Exception as e:
            logger.error(f"Failed to load ACE-Step: {e}")
            self.loader = None

    def on_model_loaded(self):
        """Handle model load completion."""
        if self.loader and self.loader.is_loaded:
            self.model_status_label.setText("🟢 ACE-Step Loaded")
            self.status_label.setText("Ready to generate!")
            self.load_model_btn.setText("Reload Model")
        else:
            self.model_status_label.setText("🔴 Load Failed")
            self.status_label.setText("Failed to load model.")
        
        self.load_model_btn.setEnabled(True)

    def refresh_voices_list(self):
        """Refresh the dropdown from the models/voices directory."""
        self.ref_audio_combo.blockSignals(True)
        self.ref_audio_combo.clear()
        self.ref_audio_combo.addItem("No Voice Selected", "")
        
        import os
        voices_dir = os.path.join(os.getcwd(), "models", "voices")
        if os.path.exists(voices_dir):
            for file in os.listdir(voices_dir):
                if file.lower().endswith(('.wav', '.mp3', '.flac', '.ogg')):
                    path = os.path.join(voices_dir, file)
                    self.ref_audio_combo.addItem(f"🎙️ {os.path.splitext(file)[0]}", path)
                    
        self.ref_audio_combo.blockSignals(False)

    def on_voice_selected(self, index):
        """Handle voice profile selection from dropdown."""
        path = self.ref_audio_combo.itemData(index)
        if path:
            self.ref_audio_path = path
            self.audio2audio_enable.setChecked(True)
        else:
            self.ref_audio_path = ""

    def browse_ref_audio(self):
        """Browse for reference audio file."""
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Reference Audio",
            "",
            "Audio Files (*.wav *.mp3 *.flac *.ogg *.m4a);;All Files (*.*)"
        )
        
        if file_path:
            self.ref_audio_path = file_path
            import os
            filename = os.path.basename(file_path)
            # Add it to combo as a temporary item
            self.ref_audio_combo.blockSignals(True)
            self.ref_audio_combo.addItem(f"📁 {filename} (Custom)", file_path)
            self.ref_audio_combo.setCurrentIndex(self.ref_audio_combo.count() - 1)
            self.ref_audio_combo.blockSignals(False)
            self.audio2audio_enable.setChecked(True)


    def generate(self):
        """Start generation."""
        if not self.loader or not self.loader.is_loaded:
             # Try to auto-load
             self.load_model()
             # Return for now, user clicks again when loaded (or we could chain it)
             return


        prompt = self.prompt_input.toPlainText()
        lyrics = self.lyrics_input.toPlainText()
        
        params = {
            "prompt": prompt,
            "lyrics": lyrics,
            "duration": self.duration_spin.value(),
            "guidance_scale": self.guidance_slider.value() / 10.0,
            "guidance_scale_lyric": self.lyric_guidance_slider.value() / 10.0,
            "infer_steps": self.steps_spin.value(),
            "seed": self.seed_spin.value(),
            "audio2audio_enable": self.audio2audio_enable.isChecked() and bool(self.ref_audio_path),
            "ref_audio_path": self.ref_audio_path if self.audio2audio_enable.isChecked() else "",
            "ref_audio_strength": self.ref_strength_slider.value() / 100.0
        }
        
        self.worker = ACEStepGenerationWorker(self.loader, params)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.status.connect(lambda s: self.status_label.setText(s))
        
        self.worker.start()
        
        self.generate_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0) # Indeterminate
        
    def stop_generation(self):
        """Stop current generation."""
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
        """Handle generation completion."""
        import os
        import soundfile as sf
        from datetime import datetime
        
        self.current_audio = audio
        self.sample_rate = self.loader.sample_rate if self.loader else 44100
        
        # Calculate duration
        duration = audio.shape[-1] / self.sample_rate
        
        # Auto-save to outputs folder
        outputs_dir = os.path.join(os.getcwd(), "outputs")
        os.makedirs(outputs_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_slug = self.prompt_input.toPlainText()[:30].replace(" ", "_").replace(",", "")
        filename = f"{timestamp}_acestep_{prompt_slug}.wav"
        filepath = os.path.join(outputs_dir, filename)
        
        try:
            # Transpose if needed (sf.write expects [samples, channels])
            if audio.ndim == 2 and audio.shape[0] == 2:
                audio_to_save = audio.T
            else:
                audio_to_save = audio
            sf.write(filepath, audio_to_save, self.sample_rate)
            logger.info(f"Auto-saved ACE-Step output: {filepath}")
            logger.info(f"  Shape: {audio.shape}, Duration: {duration:.1f}s, SR: {self.sample_rate}")
        except Exception as e:
            logger.error(f"Failed to auto-save: {e}")
        
        # Emit signal for global player
        self.play_audio.emit(self.current_audio, self.sample_rate)
        
        # Update UI
        self.audio_info_label.setText(f"✓ Generated: {duration:.1f}s | {self.sample_rate}Hz")
        
        self.generate_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        self.status_label.setText(f"Generation complete! Saved to {filename}")
    
    def on_generation_error(self, error_msg):
        """Handle generation error."""
        self.status_label.setText(f"Error: {error_msg}")
        self.generate_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)

    def on_preset_changed(self, text):
        """Handle style preset selection."""
        if not text or text == "Select a Style Preset...":
            return
            
        prompt = self.STYLE_PRESETS.get(text, "")
        if prompt:
            self.prompt_input.setText(prompt)

