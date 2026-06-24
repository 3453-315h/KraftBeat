"""
Kraftbeat - AI Text-to-Music Generator

Main PyQt6 window application.
"""

import sys
import logging
from pathlib import Path
from typing import Optional
import numpy as np

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

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QSlider,
    QProgressBar, QFileDialog, QGroupBox, QSpinBox, QDoubleSpinBox,
    QStatusBar, QSplitter, QFrame, QMessageBox, QCheckBox, QListWidget,
    QStackedWidget, QSplashScreen, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QDateTime, QObject
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon, QShortcut, QPixmap
from PyQt6.QtGui import QKeySequence

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from device import get_device, DeviceInfo, DeviceType
from models.musicgen import MusicGenLoader, MUSICGEN_MODELS, list_models
from utils.audio import save_audio, normalize_audio
from utils.streaming import StreamingGenerator

# Import from refactored modules
from ui.workers import QTextEditLogger, GenerationWorker, ModelLoadWorker, VariationWorker
from ui.themes import apply_dark_theme, apply_light_theme, DARK_STYLESHEET, LIGHT_STYLESHEET
from ui.panels.stems_panel import StemsPanel
from ui.panels.ace_step_panel import ACEStepPanel
from ui.panels.diffrhythm_panel import DiffRhythmPanel
from ui.panels.player_panel import PlayerPanel  # New Global Player
from ui.dialogs.settings_panel import SettingsPanel
from ui.dialogs.cache_dialog import ModelManagerPanel
from ui.dialogs.console_window import ConsoleWindow
from ui.panels.strudel_panel import StrudelPanel
from ui.panels.voice_panel import VoicePanel
from ui.panels.arranger_panel import ArrangerPanel
from api.api_worker import APIWorker
from api.server import set_loader as api_set_loader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("kraftbeat.log", mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Kraftbeat main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kraftbeat - AI Music Generator")
        
        # Initialize instance variables
        self.device_info: Optional[DeviceInfo] = None
        self.loader: Optional[MusicGenLoader] = None
        self.current_sample_rate = 32000
        self.generation_history = []
        self.auto_save = False  # Auto-save handled by individual panels
        self.current_prompt = ""
        self.prompt_history = []
        self.current_audio = None
        self.is_playing = False
        
        # Load settings
        from utils.config import ConfigManager
        self.app_settings = ConfigManager.instance().get_all()
        self.is_dark_theme = True
        self.console_window = None
        self.api_worker = None
        
        # Init UI
        self.init_ui()
        
        # Detect device after UI is up
        self.detect_device()
        
        # Start API server
        self._start_api_server()
        
    def init_ui(self):
        """Initialize the user interface."""
        if self.is_dark_theme:
            self.apply_dark_theme()
        
        self.resize(1200, 800)
        
        # Main Layout Container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar (Left)
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Main Content Area (Right)
        content_container = QWidget()
        container_layout = QVBoxLayout(content_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Header
        self.header = self.create_header()
        container_layout.addWidget(self.header)
        
        # Stacked Widget for Pages
        self.stack = QStackedWidget()
        self.stack.currentChanged.connect(self.on_tab_changed)
        
        # --- Page 0: Generator (Controls + History) ---
        generator_page = QWidget()
        gen_layout = QHBoxLayout(generator_page)
        gen_layout.setContentsMargins(10, 10, 10, 0) # Bottom 0 to connect with player
        
        self.controls_panel = self.create_controls_panel()
        self.output_panel = self.create_output_panel()
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.controls_panel)
        splitter.addWidget(self.output_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        gen_layout.addWidget(splitter)
        self.stack.addWidget(generator_page) # Index 0
        
        # --- Page 1: Stems ---
        self.stems_panel = StemsPanel()
        self.stack.addWidget(self.stems_panel) # Index 1
        
        # --- Page 2: Model Manager ---
        self.model_manager_panel = ModelManagerPanel(self)
        self.stack.addWidget(self.model_manager_panel) # Index 2
        
        # --- Page 3: Settings ---
        self.settings_panel = SettingsPanel(self, self.app_settings)
        self.stack.addWidget(self.settings_panel) # Index 3
        
        # --- Page 4: ACE-Step (Vocals) ---
        self.ace_step_panel = ACEStepPanel(self)
        self.ace_step_panel.play_audio.connect(self.handle_external_audio)
        self.stack.addWidget(self.ace_step_panel) # Index 4
        
        # Add stack to layout
        container_layout.addWidget(self.stack, 1)
        
        # --- Page 5: DiffRhythm (Fast Long-Form) ---
        self.diffrhythm_panel = DiffRhythmPanel(self)
        self.diffrhythm_panel.play_audio.connect(self.handle_external_audio)
        self.stack.addWidget(self.diffrhythm_panel)  # Index 5
        
        # --- Page 6: Strudel (Live Coding) ---
        self.strudel_panel = StrudelPanel(self)
        self.stack.addWidget(self.strudel_panel)  # Index 6
        
        # --- Page 7: Voice Lab ---
        self.voice_panel = VoicePanel(self)
        self.stack.addWidget(self.voice_panel)  # Index 7
        self.voice_panel.voices_updated.connect(self.ace_step_panel.refresh_voices_list)
        
        # --- Page 8: Block Arranger ---
        self.arranger_panel = ArrangerPanel(self)
        self.arranger_panel.render_ready.connect(self._on_arrangement_rendered)
        self.stack.addWidget(self.arranger_panel)  # Index 8
        
        # --- GLOBAL PLAYER PANEL (Bottom Dock) ---
        self.player_panel = PlayerPanel(self)
        container_layout.addWidget(self.player_panel)
        
        # Initialize detached console
        self.console_window = ConsoleWindow()
        self.console_window.setup_logging()
        
        main_layout.addWidget(content_container, 1)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add resource monitor label on the right side
        self.resource_label = QLabel("RAM: --")
        self.resource_label.setStyleSheet("color: #808090; padding-right: 8px;")
        self.status_bar.addPermanentWidget(self.resource_label)
        
        self.status_bar.showMessage("Ready")
        
        # Start resource monitoring timer
        self.resource_timer = QTimer(self)
        self.resource_timer.timeout.connect(self.update_resource_display)
        self.resource_timer.start(2000)  # Update every 2 seconds
        self.update_resource_display()  # Initial update
        
    def apply_dark_theme(self):
        """Apply dark color scheme."""
        palette = QPalette()
        
        # Base colors
        bg_dark = QColor(30, 30, 35)
        bg_mid = QColor(45, 45, 52)
        fg = QColor(220, 220, 225)
        accent = QColor(100, 140, 255)
        
        palette.setColor(QPalette.ColorRole.Window, bg_dark)
        palette.setColor(QPalette.ColorRole.WindowText, fg)
        palette.setColor(QPalette.ColorRole.Base, bg_mid)
        palette.setColor(QPalette.ColorRole.AlternateBase, bg_dark)
        palette.setColor(QPalette.ColorRole.Text, fg)
        palette.setColor(QPalette.ColorRole.Button, bg_mid)
        palette.setColor(QPalette.ColorRole.ButtonText, fg)
        palette.setColor(QPalette.ColorRole.Highlight, accent)
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        self.setPalette(palette)
        
        # Stylesheet for additional styling
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #404050;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }
            QPushButton {
                background-color: #648cff;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7a9fff;
            }
            QPushButton:pressed {
                background-color: #4a6cd4;
            }
            QPushButton:disabled {
                background-color: #404050;
                color: #808090;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #404050;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                width: 16px;
                height: 16px;
                background: #648cff;
                border-radius: 8px;
                margin: -5px 0;
            }
            QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 6px;
                border: 1px solid #404050;
                border-radius: 4px;
            }
            QTextEdit, QLineEdit {
                border: 1px solid #404050;
                border-radius: 4px;
                padding: 8px;
            }
            QProgressBar {
                border: 1px solid #404050;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #648cff;
                border-radius: 3px;
            }
        """)
    
    def create_sidebar(self) -> QWidget:
        """Create left vertical icon sidebar."""
        sidebar = QWidget()
        sidebar.setFixedWidth(60)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #202125;
                border-right: 1px solid #303040;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-size: 18px;
                min-width: 52px;
                max-width: 52px;
                min-height: 52px;
                max-height: 52px;
            }
            QPushButton:hover {
                background-color: #303040;
            }
            QPushButton:checked {
                background-color: #648cff;
            }
            QPushButton:pressed {
                background-color: #404050;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 16, 0, 16)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        # Define icons path
        icons_path = Path(__file__).parent / "assets" / "icons"
        from PyQt6.QtCore import QSize
        icon_size = QSize(36, 36)  # Larger icons
        
        # Logo/Home
        home_btn = QPushButton()
        home_btn.setIcon(QIcon(str(icons_path / "home.png")))
        home_btn.setIconSize(icon_size)
        home_btn.setToolTip("Home")
        home_btn.clicked.connect(self.show_generator)
        layout.addWidget(home_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        layout.addSpacing(20)
        
        # Generate View
        gen_btn = QPushButton()
        gen_btn.setIcon(QIcon(str(icons_path / "generate.png")))
        gen_btn.setIconSize(icon_size)
        gen_btn.setToolTip("Generator View (Ctrl+G)")
        gen_btn.clicked.connect(self.show_generator)
        layout.addWidget(gen_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Play
        self.sidebar_play_btn = QPushButton()
        self.sidebar_play_btn.setIcon(QIcon(str(icons_path / "play.png")))
        self.sidebar_play_btn.setIconSize(icon_size)
        self.sidebar_play_btn.setToolTip("Play/Stop (Ctrl+Space)")
        self.sidebar_play_btn.clicked.connect(self.toggle_playback)
        layout.addWidget(self.sidebar_play_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # ACE-Step (Vocals)
        ace_step_btn = QPushButton()
        ace_step_btn.setIcon(QIcon(str(icons_path / "ace_step.png")))
        ace_step_btn.setIconSize(icon_size)
        ace_step_btn.setToolTip("ACE-Step (Vocals)")
        ace_step_btn.clicked.connect(self.show_ace_step_panel)
        layout.addWidget(ace_step_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # DiffRhythm (Fast Long-Form)
        diffrhythm_btn = QPushButton()
        diffrhythm_btn.setIcon(QIcon(str(icons_path / "diffrhythm.png")))
        diffrhythm_btn.setIconSize(icon_size)
        diffrhythm_btn.setToolTip("DiffRhythm (Fast Long-Form)")
        diffrhythm_btn.clicked.connect(self.show_diffrhythm_panel)
        layout.addWidget(diffrhythm_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Stems Panel
        stems_btn = QPushButton()
        stems_btn.setIcon(QIcon(str(icons_path / "stems.png")))
        stems_btn.setIconSize(icon_size)
        stems_btn.setToolTip("Stems Mixer")
        stems_btn.clicked.connect(self.show_stems_panel)
        layout.addWidget(stems_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Strudel Live Coding
        strudel_btn = QPushButton()
        strudel_btn.setText("🎹")  # Use emoji as icon fallback
        strudel_btn.setStyleSheet("font-size: 18px; padding: 8px;")
        strudel_btn.setToolTip("Strudel Live Coding")
        strudel_btn.clicked.connect(self.show_strudel_panel)
        layout.addWidget(strudel_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Voice Lab
        voice_btn = QPushButton()
        voice_btn.setText("🎙️")
        voice_btn.setStyleSheet("font-size: 18px; padding: 8px;")
        voice_btn.setToolTip("Voice Lab (Custom Voice Cloning)")
        voice_btn.clicked.connect(self.show_voice_panel)
        layout.addWidget(voice_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Block Arranger
        arranger_btn = QPushButton()
        arranger_btn.setText("🎤")
        arranger_btn.setStyleSheet("font-size: 18px; padding: 8px;")
        arranger_btn.setToolTip("Block Arranger (Stack & Export)")
        arranger_btn.clicked.connect(self.show_arranger_panel)
        layout.addWidget(arranger_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        layout.addStretch()
        
        # Cache Manager
        cache_btn = QPushButton()
        cache_btn.setIcon(QIcon(str(icons_path / "cache.png")))
        cache_btn.setIconSize(icon_size)
        cache_btn.setToolTip("Model Manager")
        cache_btn.clicked.connect(self.show_cache_dialog)
        layout.addWidget(cache_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Microphone Recording
        self.mic_btn = QPushButton()
        self.mic_btn.setIcon(QIcon(str(icons_path / "mic.png")))
        self.mic_btn.setIconSize(icon_size)
        self.mic_btn.setToolTip("Record Melody (Click to start/stop)")
        self.mic_btn.setCheckable(True)
        self.mic_btn.clicked.connect(self.toggle_recording)
        layout.addWidget(self.mic_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Settings
        settings_btn = QPushButton()
        settings_btn.setIcon(QIcon(str(icons_path / "settings.png")))
        settings_btn.setIconSize(icon_size)
        settings_btn.setToolTip("Settings")
        settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(settings_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        return sidebar
        
    def create_header(self) -> QWidget:
        """Create header section."""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 8)
        layout.setSpacing(4)  # Tighter spacing
        
        # Title
        # Logo Icon
        logo_label = QLabel()
        logo_path = str(Path(__file__).parent / "assets" / "icon.png")
        if Path(logo_path).exists():
            pixmap = QPixmap(logo_path)
            # Scale nicely to match header text
            scaled = pixmap.scaled(42, 42, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled)
        layout.addWidget(logo_label)

        # Title Text
        title = QLabel("Kraftbeat")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("margin-left: 2px;")  # Minimal spacing
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Device info
        self.device_label = QLabel("Device: Detecting...")
        self.device_label.setStyleSheet("color: #808090;")
        layout.addWidget(self.device_label)
        
        # Console toggle button
        self.console_btn = QPushButton("📋 Console")
        self.console_btn.setCheckable(True)
        self.console_btn.setStyleSheet("""
            QPushButton {
                background-color: #404050;
                padding: 6px 12px;
            }
            QPushButton:checked {
                background-color: #648cff;
            }
        """)
        self.console_btn.clicked.connect(self.toggle_console)
        layout.addWidget(self.console_btn)
        
        return frame
        
    def create_output_panel(self) -> QWidget:
        """Create the right output panel (Simplified for Global Player)."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 0, 0, 0)
        
        # Prompt (Moved from Left)
        self.prompt_panel = self.create_prompt_panel()
        layout.addWidget(self.prompt_panel)
        
        # Generation history
        history_group = QGroupBox("History")
        history_layout = QVBoxLayout(history_group)
        
        from PyQt6.QtWidgets import QListWidget, QListWidgetItem
        self.history_list = QListWidget()
        # Make history taller now that we removed waveform/controls
        self.history_list.setMaximumHeight(400) 
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #1a1a20;
                border: 1px solid #303040;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #252530;
            }
            QListWidget::item:selected {
                background-color: #648cff;
            }
            QListWidget::item:hover {
                background-color: #303040;
            }
        """)
        self.history_list.itemDoubleClicked.connect(self.on_history_item_clicked)
        history_layout.addWidget(self.history_list)
        
        # History controls
        hist_controls = QHBoxLayout()
        clear_hist_btn = QPushButton("Clear")
        clear_hist_btn.clicked.connect(self.clear_history)
        hist_controls.addWidget(clear_hist_btn)
        hist_controls.addStretch()
        history_layout.addLayout(hist_controls)
        
        layout.addWidget(history_group)
        layout.addStretch()
        
        return panel
    
    def create_prompt_panel(self) -> QGroupBox:
        """Create the prompt configuration panel."""
        prompt_group = QGroupBox("Prompt")
        prompt_layout = QVBoxLayout(prompt_group)
        
        # Prompt history dropdown
        history_layout = QHBoxLayout()
        history_layout.addWidget(QLabel("History:"))
        self.history_combo = QComboBox()
        self.history_combo.setPlaceholderText("Previous prompts...")
        self.history_combo.currentTextChanged.connect(self.on_history_selected)
        history_layout.addWidget(self.history_combo, 1)
        prompt_layout.addLayout(history_layout)
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText(
            "Describe the music you want to generate...\\n\\n"
            "Example: 80s synthwave, pulsing bass, retro drums, neon atmosphere"
        )
        self.prompt_input.setMaximumHeight(100)
        self.prompt_input.setToolTip(
            "Describe the music you want to generate.\\n\\n"
            "Tips for better results:\\n"
            "• Include genre, instruments, mood, tempo\\n"
            "• Add '120bpm' for specific tempo\\n"
            "• Add 'key of Am' for specific key\\n"
            "• Use adjectives: energetic, mellow, dark, bright\\n\\n"
            "The prompt combines with Genre and Structure selections."
        )
        prompt_layout.addWidget(self.prompt_input)
        
        # Prompt templates (Genres)
        templates_layout = QHBoxLayout()
        templates_layout.addWidget(QLabel("Genres:"))
        self.template_combo = QComboBox()
        self.template_combo.addItem("Select a genre...", "")
        templates = [
            ("🎸 Rock", "rock music, electric guitar, powerful drums, energetic, stadium sound"),
            ("🎹 Classical", "classical orchestra, strings, piano, elegant, cinematic, emotional"),
            ("🎧 Electronic", "electronic music, synthesizers, deep bass, rhythmic, club atmosphere"),
            ("🎷 Jazz", "jazz music, saxophone, piano, double bass, smooth, improvisation"),
            ("🎤 Hip Hop", "hip hop beat, 808 bass, trap hi-hats, urban, bouncy rhythm"),
            ("🌴 Lofi", "lofi hip hop, chill beats, vinyl crackle, relaxing, study music"),
            ("🌊 Ambient", "ambient music, ethereal pads, atmospheric, peaceful, meditative"),
            ("🎻 Cinematic", "epic cinematic, orchestra, dramatic, movie soundtrack, emotional"),
            ("🎺 Funk", "funk music, groovy bass, brass section, rhythmic guitar, danceable"),
            ("🌙 Synthwave", "80s synthwave, retro synths, pulsing bass, neon atmosphere, nostalgic"),
            ("🦁 Reggae", "reggae music, offbeat guitar, heavy bass, relaxed tempo, jamaican vibe"),
            ("🛸 Techno", "techno music, 4/4 kick drum, industrial synths, repetitive, driving"),
            ("🏠 House", "house music, soulful vocals, deep bassline, 120 bpm, dance floor"),
            ("⚡ Drum & Bass", "drum and bass, breakbeats, heavy sub bass, fast tempo, energetic"),
            ("🔊 Dubstep", "dubstep, heavy wobble bass, aggressive drops, electronic, intense"),
            ("🎸 Metal", "heavy metal, distorted guitars, aggressive drums, intense, dark"),
            ("🤠 Country", "country music, acoustic guitar, storytelling, twang, folk vibe"),
            ("💙 Blues", "blues music, electric guitar solos, soulful, 12-bar blues, emotional"),
            ("✨ Disco", "disco music, funky bass, strings, four-on-the-floor, groovy, party"),
            ("🕺 Trance", "trance music, melodic synthesizers, build-ups, ethereal, uplifting"),
            ("🤎 R&B", "contemporary r&b, smooth vocals, groovy beat, soulful, urban"),
            ("🎮 Chiptune", "chiptune, 8-bit, retro video game sound, square waves, nostalgic"),
            ("🚬 Trip Hop", "trip hop, downtempo, bristol sound, massive bass, atmospheric, moody"),
            ("🥁 Breakbeat", "breakbeat, funky breaks, old school, energetic, syncopated drums"),
            ("👾 Glitch / IDM", "glitch music, idm, complex rhythms, digital noise, experimental, aphex twin style"),
            ("🏭 Industrial", "industrial music, harsh textures, metallic percussion, aggressive, dark"),
            ("🌫️ Vaporwave", "vaporwave, slowed, chopped, retro aesthetic, mallsoft, nostalgic"),
            ("🦇 Darkwave", "darkwave, gothic, dark synth, melancholic, post-punk influence"),
            ("📐 Math Rock", "math rock, complex time signatures, angular guitar, tapping, clean tone"),
            ("🧬 Experimental", "experimental music, avant-garde, abstract textures, non-linear, noise"),
            ("🌌 Ambient Drone", "ambient drone, deep textures, sustaining tones, meditative, minimal"),
        ]
        for name, prompt in templates:
            self.template_combo.addItem(name, prompt)
        self.template_combo.currentIndexChanged.connect(self.update_compound_prompt)
        self.template_combo.setToolTip(
            "Select a music genre to auto-fill the prompt.\\n"
            "Combines with Structure for complete prompts."
        )
        templates_layout.addWidget(self.template_combo, 1)
        prompt_layout.addLayout(templates_layout)
        
        # Structure templates
        structure_layout = QHBoxLayout()
        structure_layout.addWidget(QLabel("Structure:"))
        self.structure_combo = QComboBox()
        structures = [
            ("None", ""),
            # Basic sections
            ("🎬 Intro", "intro section, build-up, soft beginning, gradually rising"),
            ("🎤 Verse", "verse section, rhythmic, melodic, storytelling feel"),
            ("🎵 Chorus", "chorus section, catchy, powerful, memorable hook"),
            ("🎙️ Pre-Chorus", "pre-chorus, tension building, anticipation, leading into chorus"),
            ("🌉 Bridge", "bridge section, transition, contrast, different feel"),
            ("🎸 Solo", "solo section, instrumental, expressive, virtuoso"),
            ("🎬 Outro", "outro section, fading, conclusion, gentle ending"),
            # EDM/Electronic sections
            ("💥 Drop", "drop section, heavy bass, intense energy, peak moment, powerful"),
            ("🔨 Breakdown", "breakdown section, stripped back, minimal, building tension"),
            ("📈 Build-up", "build-up section, rising energy, snare rolls, increasing intensity"),
            ("🎹 Ambient Pad", "ambient pad section, atmospheric, sustained chords, ethereal"),
            # Rock/Metal sections
            ("🎸 Riff", "main riff section, heavy guitar, repetitive motif, driving rhythm"),
            ("🥁 Drum Break", "drum break, percussion focus, rhythmic showcase, dynamic"),
            # Additional elements
            ("🎶 Hook", "hook section, catchy melody, memorable phrase, sing-along"),
            ("🌊 Interlude", "interlude, transitional, reflective pause, connecting section"),
            ("⚡ Climax", "climax section, highest energy, emotional peak, powerful resolution"),
            ("🌙 Fade Out", "fade out ending, gradually decreasing volume, soft conclusion"),
            # Full structures
            ("🎼 Full Song", "complete song structure with intro, verse, chorus, bridge, and outro, cohesive arrangement, dynamic progression"),
            ("🎧 EDM Track", "EDM structure with intro, build-up, drop, breakdown, second drop, and outro"),
            ("🎸 Rock Song", "rock song structure with intro riff, verse, pre-chorus, chorus, guitar solo, final chorus"),
        ]
        for name, modifier in structures:
            self.structure_combo.addItem(name, modifier)
        self.structure_combo.currentIndexChanged.connect(self.update_compound_prompt)
        self.structure_combo.setToolTip(
            "Select song structure or section type.\\n\\n"
            "• Single sections: Intro, Verse, Chorus, Bridge, etc.\\n"
            "• Full structures: Complete songs with all sections\\n\\n"
            "'Full Song' enables the Dynamic Structure Engine\\n"
            "with golden ratio positioning and phase evolution."
        )
        structure_layout.addWidget(self.structure_combo, 1)
        prompt_layout.addLayout(structure_layout)
        
        # BPM and Key controls
        music_params_layout = QHBoxLayout()
        
        # BPM
        music_params_layout.addWidget(QLabel("BPM:"))
        self.bpm_spin = QSpinBox()
        self.bpm_spin.setRange(0, 300)
        self.bpm_spin.setValue(0)
        self.bpm_spin.setSpecialValueText("Auto")
        self.bpm_spin.setToolTip(
            "Tempo in beats per minute (20-300)\\n"
            "0 = Auto: Extracts from prompt (e.g., '120bpm')\\n"
            "or lets the model decide.\\n\\n"
            "Tip: Common tempos:\\n"
            "• 60-80: Ballad, Ambient\\n"
            "• 90-110: Hip Hop, R&B\\n"
            "• 120-130: House, Pop\\n"
            "• 140-180: Drum & Bass, Techno"
        )
        self.bpm_spin.setMaximumWidth(80)
        music_params_layout.addWidget(self.bpm_spin)
        
        music_params_layout.addSpacing(15)
        
        # Key
        music_params_layout.addWidget(QLabel("Key:"))
        self.key_combo = QComboBox()
        keys = [
            "Auto",
            "C major", "C minor", "C# major", "C# minor",
            "D major", "D minor", "D# major", "D# minor",
            "E major", "E minor",
            "F major", "F minor", "F# major", "F# minor",
            "G major", "G minor", "G# major", "G# minor",
            "A major", "A minor", "A# major", "A# minor",
            "B major", "B minor"
        ]
        self.key_combo.addItems(keys)
        self.key_combo.setToolTip(
            "Musical key for consistent tonality across all chunks.\\n"
            "Auto = Extracts from prompt or model decides.\\n\\n"
            "• Major keys: Bright, happy, uplifting\\n"
            "• Minor keys: Dark, sad, emotional\\n\\n"
            "Tip: Popular keys in music:\\n"
            "• C major: Neutral, clear\\n"
            "• A minor: Emotional, versatile\\n"
            "• G major: Bright, folk/rock\\n"
            "• E minor: Guitar-friendly, rock"
        )
        self.key_combo.setMaximumWidth(120)
        music_params_layout.addWidget(self.key_combo)
        
        music_params_layout.addStretch()
        prompt_layout.addLayout(music_params_layout)
        
        # Auto-save checkbox
        from PyQt6.QtWidgets import QCheckBox
        self.autosave_check = QCheckBox("Auto-save to outputs/")
        self.autosave_check.setChecked(True)
        self.autosave_check.toggled.connect(lambda v: setattr(self, 'auto_save', v))
        prompt_layout.addWidget(self.autosave_check)
        
        return prompt_group
    

        
    def create_controls_panel(self) -> QWidget:
        """Create left controls panel."""
        # Wrap everything in a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        panel = QWidget()
        scroll.setWidget(panel)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 10, 0)
        
        # Model selection
        model_group = QGroupBox("Model")
        model_layout = QVBoxLayout(model_group)
        
        self.model_combo = QComboBox()
        model_layout.addWidget(self.model_combo)
        
        self.load_model_btn = QPushButton("Load Model")
        self.load_model_btn.clicked.connect(self.load_model)
        model_layout.addWidget(self.load_model_btn)
        
        layout.addWidget(model_group)
        
        # Initialize list
        self.update_model_list()
        
        # Continue building the rest of the controls panel
        self.create_controls_panel_continued(layout)
        
        return scroll

    def update_model_list(self):
        """Update model dropdown based on cache status."""
        if not hasattr(self, 'model_combo'): return

        # Helper to preserve selection
        current_selection = self.model_combo.currentText().split(' (')[0] if self.model_combo.count() > 0 else "small"
        
        self.model_combo.clear()
        
        # Filter models - only show downloaded ones in the main dropdown
        from utils.cache import get_cached_models
        # Force refresh of cache list
        cached_list = get_cached_models()
        cached_ids = [m['name'] for m in cached_list]
        
        # Always include 'small' as fallback/default if nothing cached
        available_count = 0
        index_to_set = 0
        
        for i, (name, info) in enumerate(MUSICGEN_MODELS.items()):
            model_id = info["id"]
            # Check if cached (huggingface cache uses org/repo format)
            is_cached = any(model_id in c for c in cached_ids)
            
            # Add if cached or if it's the default 'small' model (so user can download it)
            if is_cached or name == "small":
                stereo = "🔊" if info["stereo"] else ""
                melody = "🎹" if info["melody"] else ""
                status = "✓" if is_cached else " (Download)"
                
                label = f"{name} ({info['params']}, {info['vram_gb']}GB) {stereo}{melody}{status}"
                self.model_combo.addItem(label, name)
                
                # Restore selection if possible
                if name == current_selection:
                    index_to_set = self.model_combo.count() - 1
                
                available_count += 1
                
        self.model_combo.setCurrentIndex(index_to_set)
        logger.info(f"Updated model list: {available_count} models found.")

    def create_controls_panel_continued(self, layout):
        """Continuation of create_controls_panel after model section."""
        # Note: Prompt section moved to create_prompt_panel() in Right Panel
        
        # Melody input (drag-and-drop)
        melody_group = QGroupBox("Melody Input (Optional)")
        melody_layout = QVBoxLayout(melody_group)
        
        self.melody_drop = QFrame()
        self.melody_drop.setMinimumHeight(60)
        self.melody_drop.setAcceptDrops(True)
        self.melody_drop.setStyleSheet("""
            QFrame {
                border: 2px dashed #404050;
                border-radius: 8px;
                background-color: #252530;
            }
        """)
        
        drop_layout = QVBoxLayout(self.melody_drop)
        self.melody_label = QLabel("Drop audio file here for melody conditioning")
        self.melody_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.melody_label.setStyleSheet("color: #606070; border: none;")
        drop_layout.addWidget(self.melody_label)
        
        melody_layout.addWidget(self.melody_drop)
        
        # Melody/Import buttons row
        melody_btn_layout = QHBoxLayout()
        
        self.import_audio_btn = QPushButton("🎵 Import Audio")
        self.import_audio_btn.setToolTip("Import audio file as generation seed")
        self.import_audio_btn.clicked.connect(self.import_audio)
        melody_btn_layout.addWidget(self.import_audio_btn)
        
        self.clear_melody_btn = QPushButton("Clear")
        self.clear_melody_btn.setEnabled(False)
        self.clear_melody_btn.clicked.connect(self.clear_melody)
        melody_btn_layout.addWidget(self.clear_melody_btn)
        melody_btn_layout.addStretch()
        melody_layout.addLayout(melody_btn_layout)
        
        # Imported audio info label
        self.imported_audio_label = QLabel("")
        self.imported_audio_label.setStyleSheet("color: #50c050; font-size: 11px;")
        self.imported_audio_label.setVisible(False)
        melody_layout.addWidget(self.imported_audio_label)
        
        # Use as seed checkbox
        self.use_as_seed_check = QCheckBox("Use imported audio as generation seed")
        self.use_as_seed_check.setToolTip("Use the imported audio to guide generation (audio-to-audio)")
        self.use_as_seed_check.setEnabled(False)
        melody_layout.addWidget(self.use_as_seed_check)
        
        layout.addWidget(melody_group)
        
        # Generation parameters
        params_group = QGroupBox("Parameters")
        params_layout = QVBoxLayout(params_group)
        
        # Duration
        dur_layout = QHBoxLayout()
        dur_layout.addWidget(QLabel("Duration (sec):"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 300)
        self.duration_spin.setValue(30)
        self.duration_spin.setToolTip("Length of audio to generate (max 30s per chunk)")
        dur_layout.addWidget(self.duration_spin)
        params_layout.addLayout(dur_layout)
        
        # Time estimate moved to status bar
        # time_layout = QHBoxLayout()
        # ...
        # params_layout.addLayout(time_layout)
        
        # Streaming control
        stream_layout = QHBoxLayout()
        self.stream_check = QCheckBox("Stream Generation")
        self.stream_check.setToolTip("Play audio as it generates (real-time preview)")
        stream_layout.addWidget(self.stream_check)
        stream_layout.addStretch()
        params_layout.addLayout(stream_layout)
        
        # BPM control
        bpm_layout = QHBoxLayout()
        self.bpm_check = QCheckBox("Target BPM:")
        self.bpm_check.setToolTip("Include tempo in prompt for better rhythm control")
        bpm_layout.addWidget(self.bpm_check)
        self.bpm_spin = QSpinBox()
        self.bpm_spin.setRange(20, 300)
        self.bpm_spin.setValue(120)
        self.bpm_spin.setEnabled(True)
        self.bpm_spin.setToolTip("Beats per minute (20=ambient, 120=pop, 180=fast, 300=speedcore)")
        # self.bpm_check.toggled.connect(self.bpm_spin.setEnabled)
        bpm_layout.addWidget(self.bpm_spin)
        bpm_layout.addStretch()
        params_layout.addLayout(bpm_layout)
        
        # Key/Scale selector
        key_layout = QHBoxLayout()
        self.key_check = QCheckBox("Key:")
        self.key_check.setToolTip("Target a specific musical key")
        key_layout.addWidget(self.key_check)
        self.key_combo = QComboBox()
        self.key_combo.addItems([
            "C major", "C minor", "C# major", "C# minor",
            "D major", "D minor", "D# major", "D# minor",
            "E major", "E minor", "F major", "F minor",
            "F# major", "F# minor", "G major", "G minor",
            "G# major", "G# minor", "A major", "A minor",
            "A# major", "A# minor", "B major", "B minor"
        ])
        self.key_combo.setEnabled(False)
        self.key_check.toggled.connect(self.key_combo.setEnabled)
        key_layout.addWidget(self.key_combo)
        key_layout.addStretch()
        params_layout.addLayout(key_layout)
        
        # Infinite Mode (Continuation)
        inf_layout = QHBoxLayout()
        self.infinite_check = QCheckBox("Infinite Mode (Continuation)")
        self.infinite_check.setToolTip("Generate tracks longer than 30s by chaining segments (30s chunks)")
        self.infinite_check.setChecked(False)
        inf_layout.addWidget(self.infinite_check)
        inf_layout.addStretch()
        params_layout.addLayout(inf_layout)
        
        # Structured Song Mode (Golden Ratio)
        struct_layout = QHBoxLayout()
        self.structured_check = QCheckBox("Structured Song Mode")
        self.structured_check.setToolTip(
            "When enabled, uses golden ratio chunking with song phases:\n"
            "Intro → Verse → Chorus → Bridge → Outro\n\n"
            "When disabled, uses native audiocraft long-form generation\n"
            "(simpler, but no intentional song structure)."
        )
        self.structured_check.setChecked(False)  # Default to native mode
        struct_layout.addWidget(self.structured_check)
        struct_layout.addStretch()
        params_layout.addLayout(struct_layout)
        
        # Temperature
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(QLabel("Temperature:"))
        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setRange(0, 200)
        self.temp_slider.setValue(100)
        self.temp_label = QLabel("1.0")
        self.temp_slider.valueChanged.connect(
            lambda v: self.temp_label.setText(f"{v/100:.2f}")
        )
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_label)
        params_layout.addLayout(temp_layout)
        
        # CFG Coefficient
        cfg_layout = QHBoxLayout()
        cfg_layout.addWidget(QLabel("Guidance:"))
        self.cfg_slider = QSlider(Qt.Orientation.Horizontal)
        self.cfg_slider.setRange(10, 100)
        self.cfg_slider.setValue(30)
        self.cfg_label = QLabel("3.0")
        self.cfg_slider.valueChanged.connect(
            lambda v: self.cfg_label.setText(f"{v/10:.1f}")
        )
        cfg_layout.addWidget(self.cfg_slider)
        cfg_layout.addWidget(self.cfg_label)
        params_layout.addLayout(cfg_layout)
        
        layout.addWidget(params_group)
        
        # Continuation mode checkbox
        self.continue_check = QCheckBox("Continue from last generation")
        self.continue_check.setToolTip("Extend the previous audio instead of generating new")
        self.continue_check.setEnabled(False)  # Enabled after first generation
        layout.addWidget(self.continue_check)
        
        # Seamless loop checkbox
        self.seamless_check = QCheckBox("Generate seamless loop")
        self.seamless_check.setToolTip("Create audio that loops smoothly end-to-end")
        layout.addWidget(self.seamless_check)
        
        # Generate button row
        gen_btn_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("🎵 Generate")
        self.generate_btn.setEnabled(False)
        self.generate_btn.clicked.connect(self.generate)
        self.generate_btn.setMinimumHeight(50)
        gen_btn_layout.addWidget(self.generate_btn, stretch=2)
        
        # Variations button
        self.variations_btn = QPushButton("🎲 Variations")
        self.variations_btn.setToolTip("Generate multiple variations to compare")
        self.variations_btn.setEnabled(False)
        self.variations_btn.clicked.connect(self.generate_variations)
        self.variations_btn.setMinimumHeight(50)
        gen_btn_layout.addWidget(self.variations_btn, stretch=1)
        
        # Variation count
        self.variation_count_spin = QSpinBox()
        self.variation_count_spin.setRange(2, 8)
        self.variation_count_spin.setValue(4)
        self.variation_count_spin.setToolTip("Number of variations to generate")
        self.variation_count_spin.setMinimumHeight(50)
        self.variation_count_spin.setMaximumWidth(50)
        gen_btn_layout.addWidget(self.variation_count_spin)
        
        self.queue_btn = QPushButton("📋")
        self.queue_btn.setToolTip("Add to queue (batch generate)")
        self.queue_btn.setEnabled(False)
        self.queue_btn.setMinimumHeight(50)
        self.queue_btn.setMaximumWidth(50)
        self.queue_btn.clicked.connect(self.add_to_queue)
        gen_btn_layout.addWidget(self.queue_btn)
        
        layout.addLayout(gen_btn_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        layout.addStretch()
        


    def setup_logging(self):
        """Set up logging to console panel."""
        self.log_handler = QTextEditLogger(self.console_output)
        self.log_handler.setLevel(logging.INFO)
        
        # Add handler to root logger and audiocraft/models loggers
        root_logger = logging.getLogger()
        root_logger.addHandler(self.log_handler)
        
        logging.getLogger('device').addHandler(self.log_handler)
        logging.getLogger('models').addHandler(self.log_handler)
        logging.getLogger('models.musicgen').addHandler(self.log_handler)
        
        logger.info("Kraftbeat initialized")
    
    def toggle_console(self):
        """Toggle console window visibility."""
        if self.console_window.isVisible():
            self.console_window.hide()
            self.console_btn.setChecked(False)
        else:
            self.console_window.show()
            self.console_window.raise_()
            self.console_window.activateWindow()
            self.console_btn.setChecked(True)
            
    def closeEvent(self, event):
        """Handle application closure."""
        if self.console_window:
            self.console_window.close()
        if self.api_worker and self.api_worker.isRunning():
            logger.info("Shutting down API server...")
            self.api_worker.stop()
        event.accept()
        
    def _start_api_server(self):
        """Start the embedded REST API server in the background."""
        try:
            host = self.app_settings.get("api_host", "127.0.0.1")
            port = int(self.app_settings.get("api_port", 8765))
            self.api_worker = APIWorker(host=host, port=port)
            self.api_worker.started_ok.connect(
                lambda url: (
                    self.status_bar.showMessage(f"Kraftbeat API live → {url}/docs", 5000),
                    logger.info(f"Kraftbeat API ready at {url}")
                )
            )
            self.api_worker.error.connect(
                lambda err: logger.warning(f"Kraftbeat API could not start: {err}")
            )
            self.api_worker.start()
        except Exception as e:
            logger.warning(f"Could not start API server: {e}")

    def detect_device(self):
        """Detect compute device."""
        self.status_bar.showMessage("Detecting compute device...")
        QTimer.singleShot(100, self._do_detect_device)
        
    def _do_detect_device(self):
        """Actually detect device (delayed to show UI first)."""
        try:
            self.device_info = get_device()
            self.device_label.setText(f"Device: {self.device_info}")
            
            if self.device_info.is_gpu:
                self.device_label.setStyleSheet("color: #50c050;")
            else:
                self.device_label.setStyleSheet("color: #c0a050;")
            
            self.loader = MusicGenLoader(self.device_info)
            api_set_loader(self.loader)  # Inject into REST API state
            self.status_bar.showMessage("Ready. Select a model to begin.")
            
        except Exception as e:
            self.status_bar.showMessage(f"Device detection failed: {e}")
            logger.error(f"Device detection failed: {e}")
            # Fallback to CPU
            from device import DeviceInfo, DeviceType
            self.device_info = DeviceInfo(DeviceType.CPU, "CPU (Fallback)", "cpu")
            self.loader = MusicGenLoader(self.device_info)
            self.status_bar.showMessage("Ready (CPU Fallback). Select a model to begin.")
            
    def load_model(self):
        """Load the selected model."""
        model_name = self.model_combo.currentData()
        
        self.load_model_btn.setEnabled(False)
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        
        # Get quantization setting
        settings = getattr(self, 'app_settings', {})
        precision = "fp32"
        
        if 'quant_mode' in settings:
            mode_idx = settings['quant_mode']
            if mode_idx == 1: precision = "fp16"
            elif mode_idx == 2: precision = "int8"
            elif mode_idx == 3: precision = "int4"
        elif settings.get('use_8bit', False):
            precision = "int8"
        
        if precision != "fp32":
            self.status_bar.showMessage(f"Loading {model_name} with {precision}...")
        
        self.worker = ModelLoadWorker(self.loader, model_name, precision=precision)
        self.worker.status.connect(self.status_bar.showMessage)
        self.worker.finished.connect(self.on_model_loaded)
        self.worker.start()
        
    def on_model_loaded(self, success: bool):
        """Handle model load completion."""
        self.progress_bar.setVisible(False)
        self.load_model_btn.setEnabled(True)
        
        if success:
            self.generate_btn.setEnabled(True)
            self.variations_btn.setEnabled(True)
            self.queue_btn.setEnabled(True)
            self.status_bar.showMessage("Model loaded. Ready to generate!")
        else:
            self.status_bar.showMessage("Failed to load model. Check console for errors.")
            QMessageBox.warning(self, "Error", "Failed to load model. See console for details.")
            
    def generate(self):
        """Generate audio from prompt."""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Error", "Please enter a prompt.")
            return
        
        self.current_prompt = prompt  # Store for history
            
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        # Get duration from settings
        duration = int(self.app_settings.get('default_duration', 30))
        
        # Get duration from spinbox if available, else usage default
        if hasattr(self, 'duration_spin'):
            duration = self.duration_spin.value()
        else:
            duration = 30 # Fallback

        params = {
            "prompt": prompt,
            "duration": duration,
            "temperature": self.temp_slider.value() / 100.0,
            "cfg_coef": self.cfg_slider.value() / 10.0,
            "infinite_mode": self.infinite_check.isChecked() or duration > 30,
            "structured_mode": self.structured_check.isChecked(),  # Golden ratio chunking vs native
            "melody_audio": self.melody_path if hasattr(self, 'melody_path') else None,
            # Structure Mode from Settings (Fibonacci chunks: coherent/balanced/speed)
            "structure_mode": self.app_settings.get('structure_mode', 'balanced'),
        }
        
        # ==================================================================================
        # DYNAMIC GOLDEN-RATIO PROMPT SYSTEM
        # Generates phase-aware prompts that evolve with the energy curve of the song.
        # ==================================================================================
        
        structure_name = self.structure_combo.currentText()
        
        # Check if structured generation is enabled (Full Song or long duration)
        if ("Full Song" in structure_name or duration > 30) and params['infinite_mode']:
            import numpy as np
            import math
            
            # Get chunk duration based on structure mode
            structure_mode = params['structure_mode']
            if structure_mode == 'coherent':
                chunk_dur = 8.0
                crossfade = 1.0
            elif structure_mode == 'speed':
                chunk_dur = 21.0
                crossfade = 3.0
            else:  # balanced
                chunk_dur = 13.0
                crossfade = 2.0
                
            effective_chunk = chunk_dur - crossfade
            num_chunks = int(np.ceil(duration / effective_chunk))
            if num_chunks < 1: num_chunks = 1
            
            # Parse base prompt to extract core elements
            base_prompt = prompt.replace("complete song structure with intro, verse, chorus, bridge, and outro,", "").strip()
            base_prompt = base_prompt.replace("cohesive arrangement, dynamic progression,", "").strip()
            
            # Extract BPM and Key - Priority: UI controls > prompt extraction
            import re
            
            # Check UI controls first
            ui_bpm = self.bpm_spin.value() if hasattr(self, 'bpm_spin') else 0
            ui_key = self.key_combo.currentText() if hasattr(self, 'key_combo') else "Auto"
            
            if ui_bpm > 0:
                detected_bpm = str(ui_bpm)
            else:
                # Try to extract from prompt
                bpm_match = re.search(r'(\d{2,3})\s*bpm', prompt, re.IGNORECASE)
                detected_bpm = bpm_match.group(1) if bpm_match else None
            
            if ui_key != "Auto":
                detected_key = ui_key
            else:
                # Try to extract from prompt
                key_match = re.search(r'key\s*(?:of\s*)?([A-Ga-g][#b]?\s*(?:major|minor|m)?)', prompt, re.IGNORECASE)
                detected_key = key_match.group(1).strip() if key_match else None
                
                # Also check for standalone key patterns like "Am", "C# minor"
                if not detected_key:
                    key_match2 = re.search(r'\b([A-G][#b]?)\s*(major|minor|m)?\b', prompt)
                    if key_match2:
                        detected_key = key_match2.group(0).strip()
            
            logger.info(f"Generation params: BPM={detected_bpm or 'auto'}, Key={detected_key or 'auto'}")
            
            # Golden Ratio for energy curve peak
            PHI = 0.618
            
            # Load Phase Modifiers from config/phases.json
            import json
            phases_file = Path(__file__).parent.parent.parent / "config" / "phases.json"
            
            PHASE_MODIFIERS = {
                "intro": "atmospheric intro, establishing theme, building anticipation, soft layers",
                "verse_early": "verse section, steady rhythm, storytelling, melodic foundation",
                "verse_late": "verse development, adding texture, building momentum",
                "pre_chorus": "pre-chorus tension, rising energy, anticipation",
                "chorus": "chorus hook, high energy, catchy melody, full arrangement",
                "chorus_peak": "chorus peak, maximum hooks, triumphant energy",
                "bridge": "bridge breakdown, dramatic shift, golden moment, tension release",
                "climax": "final chorus, climax, powerful crescendo, euphoric",
                "outro_early": "outro beginning, softening energy, reflecting",
                "outro_fade": "fade out, peaceful resolution, final notes, gentle ending"
            }
            
            try:
                if phases_file.exists():
                    with open(phases_file, 'r', encoding='utf-8') as f:
                        phases_data = json.load(f)
                        loaded_phases = phases_data.get('phases', {})
                        if loaded_phases:
                            PHASE_MODIFIERS.update(loaded_phases)
                            logger.info(f"Loaded custom phase modifiers from {phases_file}")
            except Exception as e:
                logger.warning(f"Failed to load phases.json, using defaults: {e}")
            
            prompt_list = []
            
            for i in range(num_chunks):
                # Calculate position (0.0 to 1.0)
                position = i / max(1, num_chunks - 1)
                
                # Calculate energy using Gaussian curve centered at golden ratio
                energy = math.exp(-((position - PHI) ** 2) / 0.08)
                
                # Determine phase based on position and energy
                if i == 0:
                    phase = "intro"
                elif i == num_chunks - 1:
                    phase = "outro_fade"
                elif position < 0.15:
                    phase = "verse_early"
                elif position < 0.25:
                    phase = "verse_late"
                elif position < 0.35:
                    phase = "pre_chorus"
                elif position < 0.50:
                    phase = "chorus"
                elif abs(position - PHI) < 0.08:  # Near golden ratio
                    phase = "bridge"
                elif position < 0.75:
                    phase = "chorus_peak"
                elif position < 0.85:
                    phase = "climax"
                else:
                    phase = "outro_early"
                
                # =====================================================
                # SUB-PROMPT AWARE MODIFIER LOOKUP
                # Phases can have sub-prompts for evolution within the phase
                # =====================================================
                
                phase_data = PHASE_MODIFIERS.get(phase, {})
                
                # Handle both old format (string) and new format (dict with base/sub_prompts)
                if isinstance(phase_data, str):
                    # Legacy format: just a string modifier
                    modifier = phase_data
                elif isinstance(phase_data, dict):
                    # New format: {base: "...", sub_prompts: [...]}
                    base_modifier = phase_data.get('base', 'developing, evolving')
                    sub_prompts = phase_data.get('sub_prompts', [])
                    
                    if sub_prompts:
                        # Calculate which sub-prompt to use within this phase
                        # We need to track how many chunks are in this phase
                        # For simplicity, use position within phase range
                        
                        # Map chunk's position to sub_prompt index
                        sub_idx = min(int(energy * len(sub_prompts)), len(sub_prompts) - 1)
                        sub_prompt = sub_prompts[sub_idx]
                        modifier = f"{base_modifier}, {sub_prompt}"
                    else:
                        modifier = base_modifier
                else:
                    modifier = "developing, evolving"
                
                # =====================================================
                # SMART SELF-AWARE PROMPT CONSTRUCTION
                # User-editable part + Auto-appended technical metadata
                # =====================================================
                
                # Calculate temperature for this chunk (same logic as workers.py)
                temp_offset = (energy - 0.5) * 0.4
                if i == 0:
                    temp_offset = -0.1
                elif i == num_chunks - 1:
                    temp_offset = -0.25
                chunk_temp = max(0.6, min(1.4, params['temperature'] + temp_offset))
                
                # Build smart prompt with locked metadata
                # Format: [user content], [phase modifier] | [technical metadata]
                # Include BPM and Key if detected from user's prompt
                bpm_str = f", bpm={detected_bpm}" if detected_bpm else ""
                key_str = f", key={detected_key}" if detected_key else ""
                
                # Also add BPM/Key to the prompt content (not just metadata)
                # This ensures the model "sees" the tempo/key in the text itself
                music_params_text = ""
                if detected_bpm:
                    music_params_text += f", {detected_bpm} bpm"
                if detected_key:
                    music_params_text += f", {detected_key}"
                
                technical_meta = (
                    f"[STRUCTURE: phase={phase}, chunk={i+1}/{num_chunks}, "
                    f"position={position*100:.0f}%, energy={energy:.2f}, temp={chunk_temp:.2f}"
                    f"{bpm_str}{key_str}]"
                )
                
                # Final prompt: base + music params + modifier + metadata
                dynamic_prompt = f"{base_prompt}{music_params_text}, {modifier} | {technical_meta}"
                prompt_list.append(dynamic_prompt)
                
                logger.debug(f"Chunk {i+1}: {phase} @ {position*100:.0f}%, modifier='{modifier[:40]}...'")
            
            # Override string prompt with dynamic list
            params["prompt"] = prompt_list
            logger.info(f"Generated dynamic prompt sequence ({num_chunks} chunks, mode={structure_mode})")
        
        if self.stream_check.isChecked() and not params['infinite_mode']:
            # Streaming Generation
            self.generate_btn.setEnabled(False)
            self.status_bar.showMessage("Streaming generation started...")
            
            if not hasattr(self, 'streamer'):
                self.streamer = StreamingGenerator(self.loader.model, self.loader.sample_rate)
            
            # Create signals helper for thread-safe updates
            class StreamSignals(QObject):
                chunk = pyqtSignal(object)
                finished = pyqtSignal(object)
            
            self.stream_signals = StreamSignals()
            self.stream_signals.chunk.connect(self.on_stream_chunk)
            self.stream_signals.finished.connect(self.on_generation_complete)
            
            def on_chunk(audio, idx):
                self.stream_signals.chunk.emit(audio)
                
            def on_complete(audio):
                self.stream_signals.finished.emit(audio)
            
            self.streamer.start_streaming(
                prompt=prompt,
                total_duration=duration,
                on_chunk=on_chunk,
                on_complete=on_complete
            )
            
        else:
            # Standard Generation
            self.worker = GenerationWorker(self.loader, params)
            self.worker.status.connect(self.status_bar.showMessage)
            self.worker.finished.connect(self.on_generation_complete)
            self.worker.error.connect(self.on_generation_error)
            self.worker.start()
            
    def on_stream_chunk(self, chunk):
        """Handle streaming audio chunk."""
        # Append chunk to current visualization (simplified)
        
    def handle_stem_generation(self, track_idx: int, prompt: str, duration: float):
        """Handle generation request from StemsPanel."""
        if not self.loader or not self.loader.model:
            QMessageBox.warning(self, "Error", "Please load a model first via the Generator tab.")
            return

        self.status_bar.showMessage(f"Generating stem: {prompt}...")
        
        # Prepare params
        params = {
            "prompt": prompt,
            "duration": duration,
            "temperature": 1.0, 
            "top_k": 250,
            "top_p": 0.0,
            "cfg_coef": 3.0,
            "infinite_mode": False
        }
        
        # Create a dedicated worker for this stem
        worker = GenerationWorker(self.loader, params)
        
        # We need to capture track_idx for the callback
        # Define callback closure
        def on_stem_finished(audio):
            if audio is not None:
                self.stems_panel.update_track_audio(track_idx, audio, self.loader.sample_rate)
                self.status_bar.showMessage(f"Stem generation complete (Track {track_idx+1})")
            else:
                self.status_bar.showMessage("Stem generation failed")
                
        worker.finished.connect(on_stem_finished)
        worker.error.connect(lambda e: self.status_bar.showMessage(f"Stem error: {e}"))
        
        # Keep reference to avoid GC
        if not hasattr(self, 'stem_workers'):
            self.stem_workers = []
        self.stem_workers.append(worker)
        
        # Clean up worker list on finish
        worker.finished.connect(lambda: self.stem_workers.remove(worker) if worker in self.stem_workers else None)
        
        worker.start()
        self.status_bar.showMessage("Generating audio stream...")
        
    def handle_external_audio(self, audio, sample_rate):
        """
        Handle audio generated by external panels (ACE-Step, DiffRhythm).
        Unified entry point for playback and visualization.
        """
        if audio is None:
            return

        self.status_bar.showMessage("Received audio from external engine...")
        
        # Ensure audio is float32
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
            
        # Update current audio state
        self.current_audio = audio
        self.current_sample_rate = sample_rate
        
        # reuse generation complete logic for visualization/history
        # We pass the audio to on_generation_complete which updates visuals
        self.on_generation_complete(audio)
        
        # Explicitly start playback
        self.play_audio()
        
    def on_generation_complete(self, audio):
        """Handle generation completion."""
        if hasattr(self, 'progress_bar'):
            self.progress_bar.setVisible(False)
        if hasattr(self, 'generate_btn'):
            self.generate_btn.setEnabled(True)
        
        self.current_audio = audio
        if self.loader:
            self.current_sample_rate = self.loader.sample_rate
        
        # Update waveform display
        if PYQTGRAPH_AVAILABLE and hasattr(self, 'waveform_curve'):
            # Flatten to mono for display if stereo
            if audio.ndim > 1:
                display_audio = audio[0] if audio.shape[0] <= 2 else audio.mean(axis=0)
            else:
                display_audio = audio
            
            # Downsample for display (max 10000 points)
            duration = len(display_audio) / self.current_sample_rate
            max_points = 10000
            if len(display_audio) > max_points:
                step = len(display_audio) // max_points
                display_audio = display_audio[::step]
            
            time_axis = np.linspace(0, duration, len(display_audio))
            self.waveform_curve.setData(time_axis, display_audio)
            
            # Update spectrogram
            self.update_spectrogram(audio)
        elif hasattr(self, 'waveform_label'):
            self.waveform_label.setText(
                f"✓ Audio generated ({audio.shape[-1] / self.current_sample_rate:.1f}s)"
            )
            self.waveform_label.setStyleSheet("color: #50c050; font-weight: bold;")
        
        # Auto-save if enabled
        if self.auto_save:
            self.auto_save_audio()
        
        # Add to prompt history
        if self.current_prompt and self.current_prompt not in self.prompt_history:
            self.prompt_history.insert(0, self.current_prompt)
            if hasattr(self, 'history_combo'):
                self.history_combo.insertItem(0, self.current_prompt[:50] + "..." if len(self.current_prompt) > 50 else self.current_prompt)
            # Keep only last 20 prompts
            if len(self.prompt_history) > 20:
                self.prompt_history = self.prompt_history[:20]
        
        # Add to generation history
        self.add_to_generation_history(self.current_prompt, audio, self.current_sample_rate)
        
        # Update playback controls (MusicGen panel only)
        if hasattr(self, 'duration_label'):
            duration_secs = len(audio.flatten()) / self.current_sample_rate if audio.ndim == 1 else len(audio[0]) / self.current_sample_rate
            mins = int(duration_secs // 60)
            secs = int(duration_secs % 60)
            self.duration_label.setText(f"{mins}:{secs:02d}")
        if hasattr(self, 'time_label'):
            self.time_label.setText("0:00")
        if hasattr(self, 'position_slider'):
            self.position_slider.setValue(0)
            self.position_slider.setEnabled(True)
        
        if hasattr(self, 'play_btn'):
            self.play_btn.setEnabled(True)
        if hasattr(self, 'stop_btn'):
            self.stop_btn.setEnabled(True)
        if hasattr(self, 'save_btn'):
            self.save_btn.setEnabled(True)
        self.status_bar.showMessage("Generation complete! Click Play to listen.")
        
    def on_generation_error(self, error: str):
        """Handle generation error."""
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        self.status_bar.showMessage(f"Error: {error}")
        QMessageBox.warning(self, "Generation Error", error)
        
    def save_audio(self):
        """Save generated audio to file with effects applied."""
        if self.current_audio is None:
            return
            
        format_ext = self.format_combo.currentText().lower()
        bitrate = self.bitrate_combo.currentText()
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Audio",
            f"kraftbeat_output.{format_ext}",
            f"{format_ext.upper()} Files (*.{format_ext})"
        )
        
        if filepath:
            # Get effect values
            reverb_wet = self.reverb_slider.value() / 100.0
            compression = self.compression_slider.value()
            bass_db = float(self.bass_slider.value())
            treble_db = float(self.treble_slider.value())
            
            # Apply effects if any are enabled
            audio = self.current_audio.copy()
            if reverb_wet > 0 or compression > 0 or bass_db != 0 or treble_db != 0:
                try:
                    from utils.effects import apply_effects_chain
                    audio = apply_effects_chain(
                        audio,
                        self.loader.sample_rate,
                        reverb_wet=reverb_wet,
                        reverb_room=0.5,
                        compression_ratio=1.0 + (compression / 25.0),  # 0-100 -> 1-5 ratio
                        compression_threshold=-20.0,
                        eq_bass=bass_db,
                        eq_mid=0.0,
                        eq_treble=treble_db,
                    )
                    self.status_bar.showMessage("Applying effects...")
                except Exception as e:
                    logger.warning(f"Effects failed: {e}")
            
            # Normalize and save
            audio = normalize_audio(audio)
            success = save_audio(
                audio,
                filepath,
                self.loader.sample_rate,
                format_ext,
                bitrate
            )
            
            if success:
                self.status_bar.showMessage(f"Saved to: {filepath}")
            else:
                QMessageBox.warning(self, "Error", "Failed to save audio file.")
    
    def update_bitrate_visibility(self, format_name: str):
        """Show/hide bitrate selector based on format."""
        lossy_formats = ["MP3", "OGG"]
        self.bitrate_combo.setEnabled(format_name.upper() in lossy_formats)
    
    def play_audio(self):
        """Play the generated audio."""
        if self.current_audio is None:
            return
        
        if not AUDIO_AVAILABLE:
            QMessageBox.warning(self, "Error", "sounddevice not installed. Cannot play audio.")
            return
        
        try:
            self.stop_audio()  # Stop any existing playback
            
            # Prepare audio for playback
            audio = self.current_audio
            if audio.ndim > 1:
                # Transpose from (channels, samples) to (samples, channels)
                audio = audio.T
            
            # Ensure float32 in valid range
            audio = np.clip(audio, -1.0, 1.0).astype(np.float32)
            
            self.is_playing = True
            if hasattr(self, 'player_panel'):
                self.player_panel.play_btn.setText("⏸")
            self.status_bar.showMessage("Playing audio...")
            
            sd.play(audio, self.current_sample_rate)
            
        except Exception as e:
            logger.error(f"Playback error: {e}")
            self.status_bar.showMessage(f"Playback error: {e}")
            self.is_playing = False
            if hasattr(self, 'player_panel'):
                self.player_panel.play_btn.setText("▶")
    
    def stop_audio(self):
        """Stop audio playback."""
        if AUDIO_AVAILABLE:
            sd.stop()
        self.is_playing = False
        if hasattr(self, 'player_panel'):
            self.player_panel.play_btn.setText("▶")
        self.status_bar.showMessage("Playback stopped.")
    
    def auto_save_audio(self):
        """Automatically save generated audio to outputs folder."""
        if self.current_audio is None:
            return
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create safe filename from prompt
        safe_prompt = "".join(c if c.isalnum() or c in " -_" else "" for c in self.current_prompt[:30]).strip()
        safe_prompt = safe_prompt.replace(" ", "_") or "generation"
        
        filename = f"{timestamp}_{safe_prompt}.wav"
        filepath = self.outputs_dir / filename
        
        audio = normalize_audio(self.current_audio)
        success = save_audio(audio, str(filepath), self.current_sample_rate, "wav")
        
        if success:
            logger.info(f"Auto-saved to: {filepath}")
            self.status_bar.showMessage(f"Auto-saved: {filename}")
        else:
            logger.warning(f"Failed to auto-save to: {filepath}")
    
    def on_history_selected(self, text: str):
        """Handle prompt history selection."""
        if text and text != "":
            # Find full prompt from history
            for prompt in self.prompt_history:
                if text.startswith(prompt[:50]):
                    self.prompt_input.setPlainText(prompt)
                    break
    
    def update_compound_prompt(self):
        """Update prompt based on selected template and structure."""
        # Get template text (if not placeholder)
        template_idx = self.template_combo.currentIndex()
        template_text = self.template_combo.itemData(template_idx)
        
        # Get structure text (if not None)
        structure_idx = self.structure_combo.currentIndex()
        structure_text = self.structure_combo.itemData(structure_idx)
        
        # Combine (Structure first, then Template)
        parts = []
        if structure_text:
            parts.append(structure_text)
        if template_text:
            parts.append(template_text)
            
        if parts:
            final_prompt = ", ".join(parts)
            self.prompt_input.setPlainText(final_prompt)
            
    def setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        from PyQt6.QtGui import QShortcut, QKeySequence
        
        # Ctrl+G = Generate
        QShortcut(QKeySequence("Ctrl+G"), self, self.generate)
        
        # Space = Play/Stop (when not in text field)
        QShortcut(QKeySequence("Ctrl+Space"), self, self.toggle_playback)
        
        # Ctrl+S = Save audio
        QShortcut(QKeySequence("Ctrl+S"), self, self.save_audio)
        
        # Ctrl+L = Load model
        QShortcut(QKeySequence("Ctrl+L"), self, self.load_model)
        
        # Escape = Stop playback
        QShortcut(QKeySequence("Escape"), self, self.stop_audio)
        
        logger.info("Keyboard shortcuts: Ctrl+G=Generate, Ctrl+Space=Play, Ctrl+S=Save, Ctrl+L=Load, Esc=Stop")
    
    def update_spectrogram(self, audio):
        """Compute and display spectrogram."""
        if not PYQTGRAPH_AVAILABLE or not hasattr(self, 'spectrogram_img'):
            return
        
        try:
            # Convert to mono
            if audio.ndim > 1:
                audio_mono = audio[0] if audio.shape[0] <= 2 else audio.mean(axis=0)
            else:
                audio_mono = audio
            
            # Spectrogram parameters
            window_size = 1024
            hop_size = 256
            
            # Compute STFT
            num_windows = (len(audio_mono) - window_size) // hop_size + 1
            if num_windows < 1:
                return
            
            # Windowing
            window = np.hanning(window_size)
            spectrogram = []
            
            for i in range(num_windows):
                start = i * hop_size
                segment = audio_mono[start:start + window_size] * window
                spectrum = np.abs(np.fft.rfft(segment))
                spectrogram.append(spectrum)
            
            spectrogram = np.array(spectrogram).T  # (freq, time)
            
            # Convert to dB
            spectrogram = 20 * np.log10(spectrogram + 1e-10)
            spectrogram = np.clip(spectrogram, -80, 0)  # Clip to -80dB floor
            
            # Normalize to 0-255 for colormap
            spectrogram = ((spectrogram + 80) / 80 * 255).astype(np.uint8)
            
            # Create colormap (viridis-like)
            lut = np.zeros((256, 4), dtype=np.uint8)
            for i in range(256):
                # Purple -> Blue -> Cyan -> Green -> Yellow
                t = i / 255.0
                if t < 0.25:
                    r, g, b = int(68 + t*4*50), int(1 + t*4*50), int(84 + t*4*80)
                elif t < 0.5:
                    r, g, b = int(50), int(100 + (t-0.25)*4*100), int(160 - (t-0.25)*4*60)
                elif t < 0.75:
                    r, g, b = int(50 + (t-0.5)*4*150), int(180), int(80 - (t-0.5)*4*80)
                else:
                    r, g, b = int(200 + (t-0.75)*4*55), int(200 - (t-0.75)*4*50), int(0)
                lut[i] = [r, g, b, 255]
            
            self.spectrogram_img.setImage(spectrogram)
            self.spectrogram_img.setLookupTable(lut)
            
            # Set proper scale
            duration = len(audio_mono) / self.current_sample_rate
            max_freq = self.current_sample_rate / 2 / 1000  # kHz
            
            self.spectrogram_widget.setXRange(0, num_windows)
            self.spectrogram_widget.setYRange(0, spectrogram.shape[0])
            
            
            # Set axis labels
            self.spectrogram_widget.setLabel('bottom', f'Time (0-{duration:.1f}s)')
            self.spectrogram_widget.setLabel('left', f'Freq (0-{max_freq:.1f}kHz)')
            
        except Exception as e:
            logger.warning(f"Spectrogram error: {e}")
            
    def on_settings_updated(self):
        """Update UI to reflect changed settings."""
        # Update duration spinbox based on default duration
        default_dur = int(self.app_settings.get('default_duration', 30))
        
        # Sync main window duration spinbox if it exists
        if hasattr(self, 'duration_spin'):
            self.duration_spin.setValue(default_dur)
             
        # Enable 8-bit quantization indicator if applicable
        use_8bit = self.app_settings.get('use_8bit', False)
        if use_8bit:
            self.device_label.setText(f"Device: {self.device_info} (8-bit)")
        else:
            self.device_label.setText(f"Device: {self.device_info}")
    
    def toggle_playback(self):
        """Toggle audio playback."""
        if self.is_playing:
            self.stop_audio()
        else:
            self.play_audio()
    
    def open_outputs_folder(self):
        """Open the outputs folder in file explorer."""
        import os
        import subprocess
        folder = str(self.outputs_dir)
        if os.path.exists(folder):
            if sys.platform == 'win32':
                subprocess.run(['explorer', folder])
            elif sys.platform == 'darwin':
                subprocess.run(['open', folder])
            else:
                subprocess.run(['xdg-open', folder])
        else:
            QMessageBox.warning(self, "Error", "Outputs folder not found.")
    
    def show_about(self):
        """Show about dialog with logo and updated info."""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtCore import Qt
        import os
        
        dialog = QDialog(self)
        dialog.setWindowTitle("About Kraftbeat")
        dialog.setFixedSize(450, 350)
        dialog.setStyleSheet("background-color: #2b2b35; color: #e0e0e0;")
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            scaled = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)
        
        # Title
        title = QLabel("<h1 style='color: #66b3ff; margin: 0;'>Kraftbeat</h1>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Version
        version = QLabel("<p style='color: #a0a0b0;'>v0.9.0</p>")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        # Subtitle
        subtitle = QLabel("<p style='color: #80c3ff;'>AI Music & Vocal Generator</p>")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Description
        desc = QLabel(
            "<p style='color: #c0c0d0;'>"
            "Generate instrumentals, full songs with vocals, and long-form compositions using cutting-edge AI models."
            "</p>"
        )
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        # Powered by section
        powered = QLabel(
            "<p style='color: #808090; margin-top: 16px;'><b>Powered by:</b><br>"
            "• <span style='color:#ffb366;'>MusicGen</span> (Meta/AudioCraft) – Instrumentals<br>"
            "• <span style='color:#66ff99;'>ACE-Step</span> – Full songs with AI vocals<br>"
            "• <span style='color:#ff66b3;'>DiffRhythm</span> – Long-form generation (4m45s)<br>"
            "• DirectML/CUDA/ROCm – GPU acceleration</p>"
        )
        powered.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(powered)
        
        layout.addStretch()
        
        # Copyright
        copy = QLabel("<p style='color: #606070;'>© 2025 Kraftbeat</p>")
        copy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copy)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(dialog.accept)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        dialog.exec()
    
    def clear_melody(self):
        """Clear the melody conditioning file."""
        self.melody_path = None
        self.melody_label.setText("🎵 Drop audio file here for melody conditioning")
        self.melody_label.setStyleSheet("color: #606070; border: none;")
        self.clear_melody_btn.setEnabled(False)
        self.status_bar.showMessage("Melody cleared")
    
    def set_melody_file(self, file_path: str):
        """Set a melody file for conditioning."""
        from pathlib import Path
        path = Path(file_path)
        
        # Check if it's an audio file
        audio_extensions = {'.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac'}
        if path.suffix.lower() not in audio_extensions:
            QMessageBox.warning(self, "Invalid File", f"Please drop an audio file ({', '.join(audio_extensions)})")
            return
        
        self.melody_path = str(path)
        self.melody_label.setText(f"✓ {path.name}")
        self.melody_label.setStyleSheet("color: #50c050; font-weight: bold; border: none;")
        self.clear_melody_btn.setEnabled(True)
        self.status_bar.showMessage(f"Melody loaded: {path.name}")
    
    def update_volume(self, value: int):
        """Update playback volume."""
        self.volume = value / 100.0
        # Update icon based on volume level
        if value == 0:
            icon = "🔇"
        elif value < 30:
            icon = "🔈"
        elif value < 70:
            icon = "🔉"
        else:
            icon = "🔊"
        self.volume_slider.setToolTip(f"Volume: {value}%")
    
    def toggle_loop(self):
        """Toggle loop playback mode."""
        self.loop_enabled = self.loop_btn.isChecked()
        if self.loop_enabled:
            self.loop_btn.setToolTip("Loop: On")
            self.status_bar.showMessage("Loop enabled - audio will repeat")
        else:
            self.loop_btn.setToolTip("Loop: Off")
            self.status_bar.showMessage("Loop disabled")
    
    def toggle_favorite(self):
        """Toggle favorite status for current audio."""
        if self.fav_btn.isChecked():
            self.fav_btn.setText("🌟")
            self.fav_btn.setToolTip("Remove from favorites")
            # Save to favorites folder
            fav_dir = self.outputs_dir / "favorites"
            fav_dir.mkdir(exist_ok=True)
            if self.current_audio is not None:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                fav_path = fav_dir / f"fav_{timestamp}.wav"
                save_audio(fav_path, self.current_audio, self.current_sr)
                self.status_bar.showMessage(f"Added to favorites: {fav_path.name}")
        else:
            self.fav_btn.setText("⭐")
            self.fav_btn.setToolTip("Add to favorites")
            self.status_bar.showMessage("Removed from favorites")
    
    def add_to_queue(self):
        """Add current prompt to generation queue."""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            self.status_bar.showMessage("Enter a prompt first")
            return
        
        # Initialize queue if needed
        if not hasattr(self, 'generation_queue'):
            self.generation_queue = []
        
        # Get duration from settings
        duration = int(self.app_settings.get('default_duration', 30))
        
        self.generation_queue.append({
            'prompt': prompt,
            'duration': duration,
            'bpm': self.bpm_spin.value() if self.bpm_check.isChecked() else None,
            'key': self.key_combo.currentText() if self.key_check.isChecked() else None
        })
        
        count = len(self.generation_queue)
        self.status_bar.showMessage(f"Added to queue ({count} items)")
        self.queue_btn.setText(f"📋{count}")
    
    def dragEnterEvent(self, event):
        """Handle drag enter event for file drops."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)
    
    def dropEvent(self, event):
        """Handle drop event for audio files."""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    self.set_melody_file(url.toLocalFile())
                    break
            event.acceptProposedAction()
        else:
            super().dropEvent(event)
    
    def update_time_estimate(self, duration: int = None):
        """Update the estimated generation time based on duration."""
        if duration is None:
            duration = self.duration_spin.value()
        
        # Rough estimates: GPU ~2.5s per second of audio, CPU ~8s per second
        if self.device_info and self.device_info.is_gpu:
            estimate = int(duration * 2.5)
        else:
            estimate = int(duration * 8)
        
        if estimate < 60:
            time_str = f"⏱️ ~{estimate}s"
        else:
            mins = estimate // 60
            secs = estimate % 60
            time_str = f"⏱️ ~{mins}m{secs}s"
        
        self.time_estimate_label.setText(time_str)
    
    def toggle_theme(self):
        """Toggle between dark and light theme."""
        self.is_dark_theme = not self.is_dark_theme
        
        if self.is_dark_theme:
            self.apply_dark_theme()
            self.theme_btn.setText("☀️")
        else:
            self.apply_light_theme()
            self.theme_btn.setText("🌙")
        
        self.status_bar.showMessage(f"Theme: {'Dark' if self.is_dark_theme else 'Light'}")
    
    def apply_light_theme(self):
        """Apply light color scheme."""
        palette = QPalette()
        
        # Base colors
        bg_light = QColor(245, 245, 250)
        bg_white = QColor(255, 255, 255)
        fg = QColor(30, 30, 35)
        accent = QColor(80, 120, 230)
        
        palette.setColor(QPalette.ColorRole.Window, bg_light)
        palette.setColor(QPalette.ColorRole.WindowText, fg)
        palette.setColor(QPalette.ColorRole.Base, bg_white)
        palette.setColor(QPalette.ColorRole.AlternateBase, bg_light)
        palette.setColor(QPalette.ColorRole.Text, fg)
        palette.setColor(QPalette.ColorRole.Button, bg_white)
        palette.setColor(QPalette.ColorRole.ButtonText, fg)
        palette.setColor(QPalette.ColorRole.Highlight, accent)
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        self.setPalette(palette)
        
        # Light theme stylesheet
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #c0c0d0;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }
            QPushButton {
                background-color: #5078e6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6088f0;
            }
            QPushButton:pressed {
                background-color: #4068c0;
            }
            QPushButton:disabled {
                background-color: #c0c0d0;
                color: #808090;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #c0c0d0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                width: 16px;
                height: 16px;
                background: #5078e6;
                border-radius: 8px;
                margin: -5px 0;
            }
            QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 6px;
                border: 1px solid #c0c0d0;
                border-radius: 4px;
                background: white;
            }
            QTextEdit, QLineEdit {
                border: 1px solid #c0c0d0;
                border-radius: 4px;
                padding: 8px;
                background: white;
            }
            QProgressBar {
                border: 1px solid #c0c0d0;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #5078e6;
                border-radius: 3px;
            }
        """)
    
    def add_to_generation_history(self, prompt: str, audio, sample_rate: int):
        """Add a generation to the history list."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Store data
        self.generation_history.insert(0, {
            "prompt": prompt,
            "audio": audio.copy(),
            "sample_rate": sample_rate,
            "timestamp": timestamp
        })
        
        # Keep only last 10 generations
        if len(self.generation_history) > 10:
            self.generation_history = self.generation_history[:10]
        
        # Add to list widget
        display_text = f"[{timestamp}] {prompt[:40]}..." if len(prompt) > 40 else f"[{timestamp}] {prompt}"
        from PyQt6.QtWidgets import QListWidgetItem
        item = QListWidgetItem(display_text)
        item.setData(256, 0)  # Store index in user role
        self.history_list.insertItem(0, item)
        
        # Keep list widget in sync
        while self.history_list.count() > 10:
            self.history_list.takeItem(self.history_list.count() - 1)
    
    def on_history_item_clicked(self, item):
        """Handle double-click on history item to load and play."""
        row = self.history_list.row(item)
        if row < len(self.generation_history):
            entry = self.generation_history[row]
            self.current_audio = entry["audio"]
            self.current_sample_rate = entry["sample_rate"]
            self.current_prompt = entry["prompt"]
            
            # Update waveform
            if PYQTGRAPH_AVAILABLE and hasattr(self, 'waveform_curve'):
                audio = self.current_audio
                if audio.ndim > 1:
                    display_audio = audio[0] if audio.shape[0] <= 2 else audio.mean(axis=0)
                else:
                    display_audio = audio
                
                duration = len(display_audio) / self.current_sample_rate
                max_points = 10000
                if len(display_audio) > max_points:
                    step = len(display_audio) // max_points
                    display_audio = display_audio[::step]
                
                time_axis = np.linspace(0, duration, len(display_audio))
                self.waveform_curve.setData(time_axis, display_audio)
            
            # Enable playback
            if hasattr(self, 'player_panel'):
                self.player_panel.play_btn.setEnabled(True)
            if hasattr(self, 'stop_btn'):
                self.stop_btn.setEnabled(True)
            if hasattr(self, 'save_btn'):
                self.save_btn.setEnabled(True)
            
            # Auto-play
            self.play_audio()
            self.status_bar.showMessage(f"Loaded: {entry['prompt'][:50]}...")
    
    def clear_history(self):
        """Clear generation history."""
        self.generation_history.clear()
        self.history_list.clear()
        self.status_bar.showMessage("History cleared.")
    
    def show_stems_panel(self):
        """Show the stems mixer panel in a dialog."""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("🎚️ Stems Mixer - Build Tracks Layer by Layer")
        dialog.setMinimumSize(900, 700)
        dialog.resize(1000, 800)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create stems panel
        stems_panel = StemsPanel()
        layout.addWidget(stems_panel)
        
        # Connect generate signal to our generation logic
        def on_stem_generate(stem_name, prompt, duration):
            # Append stem-specific modifier to prompt
            full_prompt = f"{prompt}, {stem_name.lower()} only, isolated {stem_name.lower()} track"
            self.prompt_edit.setText(full_prompt)
            self.duration_spin.setValue(int(duration))
            self.status_bar.showMessage(f"Generating {stem_name} stem: {prompt}")
            self.start_generation()
        
        # Connect each stem track's generate signal
        for stem_track in stems_panel.stem_tracks:
            stem_track.generate_requested.connect(on_stem_generate)
        
        # Apply current theme
        if self.is_dark_theme:
            dialog.setStyleSheet(DARK_STYLESHEET)
        else:
            dialog.setStyleSheet(LIGHT_STYLESHEET)
        
        dialog.exec()
    
    def save_project(self):
        """Save current session to a project file."""
        from utils.project import create_project_data, save_project
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project",
            "my_project.kraftbeat",
            "Kraftbeat Project (*.kraftbeat)"
        )
        
        if not filepath:
            return
        
        # Gather current settings
        project_data = create_project_data(
            prompt=self.prompt_edit.toPlainText(),
            duration=self.duration_spin.value(),
            temperature=self.temp_slider.value() / 100.0,
            model_name=self.model_combo.currentText(),
            bpm_enabled=self.bpm_checkbox.isChecked() if hasattr(self, 'bpm_checkbox') else False,
            bpm=self.bpm_spin.value() if hasattr(self, 'bpm_spin') else 120,
            key_enabled=self.key_checkbox.isChecked() if hasattr(self, 'key_checkbox') else False,
            key_name=self.key_combo.currentText() if hasattr(self, 'key_combo') else "C Major",
            continuation_mode=self.continuation_checkbox.isChecked() if hasattr(self, 'continuation_checkbox') else False,
            seamless_loop=self.seamless_checkbox.isChecked() if hasattr(self, 'seamless_checkbox') else False,
            reverb=self.reverb_slider.value() if hasattr(self, 'reverb_slider') else 0,
            compression=self.compression_slider.value() if hasattr(self, 'compression_slider') else 0,
            bass_eq=self.bass_slider.value() if hasattr(self, 'bass_slider') else 0,
            treble_eq=self.treble_slider.value() if hasattr(self, 'treble_slider') else 0,
            format_type=self.format_combo.currentText(),
            bitrate=self.bitrate_combo.currentText() if hasattr(self, 'bitrate_combo') else "192k",
            notes=self.notes_input.text() if hasattr(self, 'notes_input') else "",
        )
        
        if save_project(filepath, project_data):
            self.status_bar.showMessage(f"Project saved: {filepath}")
        else:
            QMessageBox.warning(self, "Error", "Failed to save project.")
    
    def open_project(self):
        """Load a project file and restore session state."""
        from utils.project import load_project
        
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            "",
            "Kraftbeat Project (*.kraftbeat)"
        )
        
        if not filepath:
            return
        
        project_data = load_project(filepath)
        if not project_data:
            QMessageBox.warning(self, "Error", "Failed to load project.")
            return
        
        # Restore settings
        self.prompt_edit.setPlainText(project_data.get("prompt", ""))
        self.duration_spin.setValue(project_data.get("duration", 10))
        self.temp_slider.setValue(int(project_data.get("temperature", 1.0) * 100))
        
        # Model
        model_name = project_data.get("model_name", "")
        idx = self.model_combo.findText(model_name)
        if idx >= 0:
            self.model_combo.setCurrentIndex(idx)
        
        # BPM
        if hasattr(self, 'bpm_checkbox'):
            self.bpm_checkbox.setChecked(project_data.get("bpm_enabled", False))
            self.bpm_spin.setValue(project_data.get("bpm", 120))
        
        # Key
        if hasattr(self, 'key_checkbox'):
            self.key_checkbox.setChecked(project_data.get("key_enabled", False))
            key_idx = self.key_combo.findText(project_data.get("key_name", "C Major"))
            if key_idx >= 0:
                self.key_combo.setCurrentIndex(key_idx)
        
        # Continuation/Loop
        if hasattr(self, 'continuation_checkbox'):
            self.continuation_checkbox.setChecked(project_data.get("continuation_mode", False))
        if hasattr(self, 'seamless_checkbox'):
            self.seamless_checkbox.setChecked(project_data.get("seamless_loop", False))
        
        # Effects
        effects = project_data.get("effects", {})
        if hasattr(self, 'reverb_slider'):
            self.reverb_slider.setValue(effects.get("reverb", 0))
        if hasattr(self, 'compression_slider'):
            self.compression_slider.setValue(effects.get("compression", 0))
        if hasattr(self, 'bass_slider'):
            self.bass_slider.setValue(effects.get("bass_eq", 0))
        if hasattr(self, 'treble_slider'):
            self.treble_slider.setValue(effects.get("treble_eq", 0))
        
        # Export settings
        export = project_data.get("export", {})
        format_idx = self.format_combo.findText(export.get("format", "WAV"))
        if format_idx >= 0:
            self.format_combo.setCurrentIndex(format_idx)
        if hasattr(self, 'bitrate_combo'):
            bitrate_idx = self.bitrate_combo.findText(export.get("bitrate", "192k"))
            if bitrate_idx >= 0:
                self.bitrate_combo.setCurrentIndex(bitrate_idx)
        
        # Notes
        if hasattr(self, 'notes_input'):
            self.notes_input.setText(project_data.get("notes", ""))
        
        self.status_bar.showMessage(f"Project loaded: {filepath}")
    
    def show_generator(self):
        """Show the main generator view."""
        self.stack.setCurrentIndex(0)
        
    def show_stems_panel(self):
        """Show the Stems Mixer panel."""
        self.stack.setCurrentIndex(1)
            
    def show_cache_dialog(self):
        """Show the Model Manager panel."""
        self.stack.setCurrentIndex(2) # Switch to Model Manager tab
        
        # We need to refresh the manager panel itself when shown
        if hasattr(self, 'model_manager_panel'):
            self.model_manager_panel.refresh_all()

    def on_tab_changed(self, index):
        """Handle tab switching events."""
        # If switching TO the generator tab (index 0)
        if index == 0:
            self.update_model_list()
        
    def show_settings(self):
        """Show the Settings panel."""
        self.stack.setCurrentIndex(3)
    
    def show_ace_step_panel(self):
        """Show the ACE-Step panel."""
        self.stack.setCurrentIndex(4)
    
    def show_diffrhythm_panel(self):
        """Show the DiffRhythm panel."""
        self.stack.setCurrentIndex(5)
    
    def show_strudel_panel(self):
        """Show the Strudel Live Coding panel and push keyboard focus into it."""
        self.stack.setCurrentIndex(6)
        # Give Chromium keyboard focus after the stack switch animation settles
        QTimer.singleShot(100, lambda: (
            self.strudel_panel.web_view.setFocus(Qt.FocusReason.OtherFocusReason)
            if self.strudel_panel.web_view else None
        ))
        
    def show_voice_panel(self):
        """Show the Voice Lab panel."""
        self.stack.setCurrentIndex(7)
    
    def show_arranger_panel(self):
        """Show the Block Arranger panel."""
        self.stack.setCurrentIndex(8)
    
    def _on_arrangement_rendered(self, path: str):
        """Called when a render completes; push audio to the global player."""
        try:
            import soundfile as sf
            data, sr = sf.read(path, always_2d=False)
            self.handle_external_audio(data, sr)
        except Exception as e:
            logger.warning(f"Could not auto-load rendered arrangement into player: {e}")
    
    def toggle_recording(self):
        """Toggle microphone recording for melody input."""
        if not hasattr(self, 'recorder'):
            from utils.recorder import AudioRecorder, RECORDING_AVAILABLE
            if not RECORDING_AVAILABLE:
                QMessageBox.warning(self, "Error", "Recording not available. Install sounddevice.")
                self.mic_btn.setChecked(False)
                return
            self.recorder = AudioRecorder(sample_rate=32000, max_duration=30.0)
        
        if self.mic_btn.isChecked():
            # Start recording
            self.mic_btn.setText("🔴")
            self.mic_btn.setToolTip("Recording... Click to stop")
            self.status_bar.showMessage("🎤 Recording melody (max 30s)...")
            
            def on_recording_done(audio, sr):
                self.recorded_melody = audio
                self.recorded_melody_sr = sr
                self.status_bar.showMessage(f"🎤 Recorded {len(audio)/sr:.1f}s of melody")
            
            success = self.recorder.start_recording(callback=on_recording_done)
            if not success:
                self.mic_btn.setChecked(False)
                self.mic_btn.setText("🎤")
                QMessageBox.warning(self, "Error", "Failed to start recording.")
        else:
            # Stop recording
            self.mic_btn.setText("🎤")
            self.mic_btn.setToolTip("Record Melody (Click to start/stop)")
            audio = self.recorder.stop_recording()
            if audio is not None:
                self.status_bar.showMessage(f"🎤 Melody recorded: {len(audio)/self.recorder.sample_rate:.1f}s")
            else:
                self.status_bar.showMessage("Recording cancelled")
    
    def update_memory_display(self):
        """Update memory status display in sidebar."""
        try:
            from utils.performance import get_memory_stats, format_bytes
            
            stats = get_memory_stats()
            
            # Build tooltip
            lines = [
                f"RAM: {format_bytes(stats.ram_used)} / {format_bytes(stats.ram_total)} ({stats.ram_percent:.0f}%)"
            ]
            
            if stats.vram_total > 0:
                lines.append(f"VRAM: {format_bytes(stats.vram_used)} / {format_bytes(stats.vram_total)} ({stats.vram_percent:.0f}%)")
                lines.append(f"GPU: {stats.device_name}")
            
            self.memory_label.setToolTip("\n".join(lines))
            
            # Color code based on usage
            if stats.ram_percent > 90 or stats.vram_percent > 90:
                self.memory_label.setText("🔴")  # High usage
            elif stats.ram_percent > 70 or stats.vram_percent > 70:
                self.memory_label.setText("🟡")  # Medium usage
            else:
                self.memory_label.setText("🟢")  # Low usage
                
        except Exception as e:
            self.memory_label.setToolTip(f"Memory: Error - {e}")
    
    def update_resource_display(self):
        """Update resource usage in status bar."""
        try:
            from utils.performance import get_memory_stats, format_bytes
            
            stats = get_memory_stats()
            
            # Format status bar text
            ram_text = f"RAM: {format_bytes(stats.ram_used)} / {format_bytes(stats.ram_total)} ({stats.ram_percent:.0f}%)"
            
            if stats.vram_total > 0:
                vram_text = f" | VRAM: {format_bytes(stats.vram_used)} / {format_bytes(stats.vram_total)} ({stats.vram_percent:.0f}%)"
                self.resource_label.setText(ram_text + vram_text)
            else:
                self.resource_label.setText(ram_text)
                
        except Exception as e:
            self.resource_label.setText(f"RAM: Error")
    
    def import_audio(self):
        """Import an audio file for use as generation seed."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Audio",
            "",
            "Audio Files (*.wav *.mp3 *.flac *.ogg *.m4a)"
        )
        
        if not file_path:
            return
        
        try:
            from utils.audio import load_audio
            result = load_audio(file_path, target_sr=32000)
            
            if result is None:
                QMessageBox.warning(self, "Error", "Failed to load audio file.")
                return
            
            audio, sr = result
            self.imported_audio = audio
            self.imported_audio_sr = sr
            self.imported_audio_path = file_path
            
            # Calculate duration
            if audio.ndim > 1:
                duration = audio.shape[1] / sr
            else:
                duration = len(audio) / sr
            
            # Update UI
            filename = Path(file_path).name
            self.imported_audio_label.setText(f"✓ {filename} ({duration:.1f}s)")
            self.imported_audio_label.setVisible(True)
            self.use_as_seed_check.setEnabled(True)
            self.use_as_seed_check.setChecked(True)
            self.clear_melody_btn.setEnabled(True)
            
            self.status_bar.showMessage(f"Imported: {filename}")
            logger.info(f"Imported audio: {filename}, {duration:.1f}s @ {sr}Hz")
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to import audio: {e}")
            logger.error(f"Audio import error: {e}")
    
    def clear_melody(self):
        """Clear the melody conditioning file and imported audio."""
        self.melody_path = None
        self.imported_audio = None
        self.imported_audio_path = None
        
        self.melody_label.setText("Drop audio file here for melody conditioning")
        self.melody_label.setStyleSheet("color: #606070; border: none;")
        self.imported_audio_label.setVisible(False)
        self.use_as_seed_check.setChecked(False)
        self.use_as_seed_check.setEnabled(False)
        self.clear_melody_btn.setEnabled(False)
        
        self.status_bar.showMessage("Cleared melody/imported audio")
    
    def generate_variations(self):
        """Generate multiple variations of the current prompt."""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Error", "Please enter a prompt.")
            return
        
        if self.loader is None or self.loader.model is None:
            QMessageBox.warning(self, "Error", "Please load a model first.")
            return
        
        variation_count = self.variation_count_spin.value()
        
        # Disable buttons and show progress
        self.generate_btn.setEnabled(False)
        self.variations_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        # Build params (use shorter duration for variations)
        duration = min(self.duration_spin.value(), 30)  # Cap at 30s for variations
        
        params = {
            "prompt": prompt,
            "duration": duration,
            "temperature": self.temp_slider.value() / 100.0,
            "cfg_coef": self.cfg_slider.value() / 10.0,
            "melody_audio": self.melody_path if self.melody_path else None,
        }
        
        # Start variation worker
        self.variations = []
        self.variation_worker = VariationWorker(self.loader, params, variation_count)
        self.variation_worker.status.connect(self.status_bar.showMessage)
        self.variation_worker.progress.connect(self.progress_bar.setValue)
        self.variation_worker.variation_complete.connect(self.on_variation_complete)
        self.variation_worker.all_complete.connect(self.on_all_variations_complete)
        self.variation_worker.error.connect(self.on_variation_error)
        self.variation_worker.start()
    
    def on_variation_complete(self, index: int, audio):
        """Handle a single variation completion."""
        self.variations.append((audio, self.loader.sample_rate))
        self.status_bar.showMessage(f"Variation {index + 1} complete")
    
    def on_all_variations_complete(self, all_audio: list):
        """Handle all variations complete."""
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        self.variations_btn.setEnabled(True)
        
        if not all_audio:
            return
        
        # Auto-save all variations if auto-save is enabled
        if self.auto_save:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            prompt = self.prompt_input.toPlainText().strip()[:30].replace(" ", "_").replace(",", "")
            
            # Create variations subfolder
            variations_dir = self.outputs_dir / "variations"
            variations_dir.mkdir(exist_ok=True)
            
            for i, audio in enumerate(all_audio):
                filename = f"{timestamp}_{prompt}_var{i+1}.wav"
                filepath = variations_dir / filename
                save_audio(filepath, audio, self.loader.sample_rate)
            
            self.status_bar.showMessage(f"Saved {len(all_audio)} variations to outputs/variations/")
        
        # Show popup to select variation
        from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QScrollArea
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Select Variation (1-{len(all_audio)})")
        dialog.setMinimumSize(500, 300)
        
        layout = QVBoxLayout(dialog)
        
        info = QLabel(f"Generated {len(all_audio)} variations. Click a variation to preview, then select one to use.")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Variation buttons
        btn_layout = QHBoxLayout()
        self._selected_variation = 0
        
        for i, audio in enumerate(all_audio):
            btn = QPushButton(f"#{i+1}")
            btn.setMinimumHeight(60)
            btn.setToolTip(f"Variation {i+1} - Click to preview")
            
            def make_preview(idx, aud):
                def preview():
                    self._selected_variation = idx
                    # Play preview
                    if AUDIO_AVAILABLE:
                        sd.stop()
                        mono = aud[0] if aud.ndim > 1 else aud
                        sd.play(mono.astype(np.float32), self.loader.sample_rate)
                    self.status_bar.showMessage(f"Previewing variation {idx + 1}")
                return preview
            
            btn.clicked.connect(make_preview(i, audio))
            btn_layout.addWidget(btn)
        
        layout.addLayout(btn_layout)
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Use selected variation
            selected_audio = all_audio[self._selected_variation]
            self.on_generation_complete(selected_audio)
            self.status_bar.showMessage(f"Using variation {self._selected_variation + 1}")
        else:
            sd.stop() if AUDIO_AVAILABLE else None
            self.status_bar.showMessage("Variation selection cancelled")
    
    def on_variation_error(self, error: str):
        """Handle variation generation error."""
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        self.variations_btn.setEnabled(True)
        QMessageBox.warning(self, "Error", f"Variation generation failed: {error}")


def main():
    """Application entry point."""
    try:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        
        # Splash Screen
        import random
        import time
        splash_dir = Path(__file__).parent / "assets" / "splash"
        splash_images = list(splash_dir.glob("*.png"))
        
        splash = None
        if splash_images:
            splash_path = random.choice(splash_images)
            pixmap = QPixmap(str(splash_path))
            # Scale if too large (e.g. keep width <= 800)
            if pixmap.width() > 800:
                pixmap = pixmap.scaledToWidth(800, Qt.TransformationMode.SmoothTransformation)
                
            splash = QSplashScreen(pixmap)
            splash.show()
            
            # Start event loop processing for splash
            t_start = time.time()
            while time.time() - t_start < 2.0:  # Show for 2 seconds max
                app.processEvents()
                time.sleep(0.01)
        
        window = MainWindow()
        window.show()
        
        if splash:
            splash.finish(window)
        
        sys.exit(app.exec())
    except Exception as e:
        import traceback
        logger.critical(f"CRITICAL ERROR: {e}", exc_info=True)
        # Keep window open to see error if it was a console window
        print(f"CRITICAL ERROR: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
