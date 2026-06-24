"""Model Manager Panel for Kraftbeat.

Displays available and installed AI music generation models with proper names,
descriptions, and technical specifications.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QMessageBox, QHeaderView, QTabWidget, QWidget,
    QProgressBar, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


# Full model catalog with proper display names
# Full model catalog imported from shared module
from models.catalog import MODEL_CATALOG


class ModelManagerPanel(QWidget):
    """Panel to manage and download models."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setup_ui()
        self.load_installed()
        self.load_catalog()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        header = QLabel("📦 Model Manager")
        header.setStyleSheet("font-size: 22px; font-weight: bold;")
        header_layout.addWidget(header)
        
        header_layout.addStretch()
        
        # Models location info
        from utils.cache import _MODELS_DIR
        location_label = QLabel(f"📁 Models stored in: {_MODELS_DIR}")
        location_label.setStyleSheet("color: #888; font-size: 11px;")
        header_layout.addWidget(location_label)
        
        layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #404050;
                border-radius: 8px;
                padding: 10px;
            }
            QTabBar::tab {
                padding: 8px 20px;
                margin-right: 5px;
                border-radius: 5px 5px 0 0;
            }
            QTabBar::tab:selected {
                background-color: #648cff;
            }
        """)
        layout.addWidget(self.tabs)
        
        # Tab 1: Model Catalog (Download)
        self.catalog_tab = QWidget()
        self.setup_catalog_tab(self.catalog_tab)
        self.tabs.addTab(self.catalog_tab, "🎵 Available Models")
        
        # Tab 2: Installed Models
        self.installed_tab = QWidget()
        self.setup_installed_tab(self.installed_tab)
        self.tabs.addTab(self.installed_tab, "💾 Installed Models")
        
        # Tab 3: Strudel Sample Packs
        self.strudel_samples_tab = QWidget()
        self.setup_strudel_samples_tab(self.strudel_samples_tab)
        self.tabs.addTab(self.strudel_samples_tab, "🎹 Strudel Samples")
        
        # Progress Bar (Global for dialog)
        self.progress_group = QGroupBox("Download Progress")
        self.progress_group.setVisible(False)
        self.progress_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #648cff;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        prog_layout = QVBoxLayout(self.progress_group)
        
        self.progress_label = QLabel("Ready")
        prog_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate by default
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #404050;
                border-radius: 5px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #648cff;
            }
        """)
        prog_layout.addWidget(self.progress_bar)
        
        layout.addWidget(self.progress_group)

    def setup_catalog_tab(self, parent):
        layout = QVBoxLayout(parent)
        layout.setSpacing(10)
        
        # Info bar
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #252530;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        info_layout = QHBoxLayout(info_frame)
        
        info = QLabel("💡 Select a model to download. Larger models produce higher quality but require more VRAM.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #aaa;")
        info_layout.addWidget(info)
        
        layout.addWidget(info_frame)
        
        # Engine sub-tabs
        self.engine_tabs = QTabWidget()
        self.engine_tabs.setStyleSheet("""
            QTabBar::tab {
                padding: 6px 16px;
                margin-right: 3px;
                border-radius: 4px 4px 0 0;
                background-color: #353545;
            }
            QTabBar::tab:selected {
                background-color: #505070;
            }
        """)
        
        # Create tables for each engine
        self.engine_tables = {}
        
        # MusicGen tab
        musicgen_tab = QWidget()
        self.engine_tables['MusicGen'] = self._create_engine_table(musicgen_tab)
        self.engine_tabs.addTab(musicgen_tab, "🎵 MusicGen")
        
        # AudioGen tab
        audiogen_tab = QWidget()
        self.engine_tables['AudioGen'] = self._create_engine_table(audiogen_tab)
        self.engine_tabs.addTab(audiogen_tab, "🔊 AudioGen")
        
        # MAGNeT tab
        magnet_tab = QWidget()
        self.engine_tables['MAGNeT'] = self._create_engine_table(magnet_tab)
        self.engine_tabs.addTab(magnet_tab, "⚡ MAGNeT")
        
        # ACE-Step tab
        acestep_tab = QWidget()
        self.engine_tables['ACESTEP'] = self._create_engine_table(acestep_tab)
        self.engine_tabs.addTab(acestep_tab, "🎤 ACE-Step")
        
        # DiffRhythm tab
        diffrhythm_tab = QWidget()
        self.engine_tables['DIFFRHYTHM'] = self._create_engine_table(diffrhythm_tab)
        self.engine_tabs.addTab(diffrhythm_tab, "🥁 DiffRhythm")
        
        layout.addWidget(self.engine_tabs)
    
    def _create_engine_table(self, parent) -> QTableWidget:
        """Create a model table for an engine tab."""
        layout = QVBoxLayout(parent)
        
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels([
            "Model Name", "Parameters", "VRAM", "Download", "Quality", "Speed", "Features", "Action"
        ])
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, 8):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        
        table.verticalHeader().setDefaultSectionSize(40)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                gridline-color: #353545;
                border: 1px solid #404050;
                border-radius: 8px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:alternate {
                background-color: #252530;
            }
            QHeaderView::section {
                background-color: #303040;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(table)
        return table

    def setup_installed_tab(self, parent):
        layout = QVBoxLayout(parent)
        layout.setSpacing(10)
        
        # Stats bar
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: #252530;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        stats_layout = QHBoxLayout(stats_frame)
        
        self.size_label = QLabel("Loading installed models...")
        self.size_label.setStyleSheet("font-weight: bold;")
        stats_layout.addWidget(self.size_label)
        
        stats_layout.addStretch()
        
        layout.addWidget(stats_frame)
        
        # Table
        self.installed_table = QTableWidget()
        self.installed_table.setColumnCount(5)
        self.installed_table.setHorizontalHeaderLabels([
            "Model Name", "Family", "Disk Size", "Last Used", "Status"
        ])
        
        header = self.installed_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        # Row height
        self.installed_table.verticalHeader().setDefaultSectionSize(40)
        self.installed_table.verticalHeader().setVisible(False)
        
        self.installed_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.installed_table.setAlternatingRowColors(True)
        self.installed_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #353545;
                border: 1px solid #404050;
                border-radius: 8px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:alternate {
                background-color: #252530;
            }
            QHeaderView::section {
                background-color: #303040;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.installed_table)
        
        # Actions
        btn_layout = QHBoxLayout()
        
        self.delete_btn = QPushButton("🗑️ Delete Selected")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #cc4444;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dd5555;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_selected)
        btn_layout.addWidget(self.delete_btn)
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #404050;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #505060;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_all)
        btn_layout.addWidget(self.refresh_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def setup_strudel_samples_tab(self, parent):
        """Setup Strudel sample packs tab."""
        from pathlib import Path
        
        layout = QVBoxLayout(parent)
        layout.setSpacing(10)
        
        # Info bar
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #252530;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        
        info = QLabel(
            "🎹 <b>Strudel Sample Packs</b><br>"
            "<span style='color: #a0a0a0;'>Download sample packs for offline live coding. "
            "Essential packs enable drum patterns like <code>s(\"bd sd\")</code>.</span>"
        )
        info.setWordWrap(True)
        info_layout.addWidget(info)
        
        layout.addWidget(info_frame)
        
        # Sample packs table
        self.strudel_table = QTableWidget()
        self.strudel_table.setColumnCount(5)
        self.strudel_table.setHorizontalHeaderLabels([
            "Sample Pack", "Category", "Size", "Status", "Action"
        ])
        
        header = self.strudel_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, 5):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        
        self.strudel_table.verticalHeader().setDefaultSectionSize(40)
        self.strudel_table.verticalHeader().setVisible(False)
        self.strudel_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.strudel_table.setAlternatingRowColors(True)
        self.strudel_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #353545;
                border: 1px solid #404050;
                border-radius: 8px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:alternate {
                background-color: #252530;
            }
            QHeaderView::section {
                background-color: #303040;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.strudel_table)
        
        # Load sample catalog
        self.load_strudel_samples()
    
    def load_strudel_samples(self):
        """Load and display Strudel sample packs."""
        from pathlib import Path
        
        try:
            from strudel.sample_catalog import STRUDEL_SAMPLE_CATALOG
        except ImportError:
            # Fallback if catalog not found
            self.strudel_table.setRowCount(1)
            item = QTableWidgetItem("Sample catalog not found")
            self.strudel_table.setItem(0, 0, item)
            return
        
        # Check which packs are installed
        samples_dir = Path(__file__).parent.parent.parent.parent / "strudel_samples"
        
        self.strudel_table.setRowCount(len(STRUDEL_SAMPLE_CATALOG))
        
        for row, (key, info) in enumerate(STRUDEL_SAMPLE_CATALOG.items()):
            # Check if installed
            pack_dir = samples_dir / key
            is_installed = pack_dir.exists() and any(pack_dir.iterdir()) if pack_dir.exists() else False
            
            # Name with essential indicator
            name = info['display_name']
            if info.get('essential', False):
                name = "⭐ " + name
            item_name = QTableWidgetItem(name)
            item_name.setToolTip(info['description'])
            self.strudel_table.setItem(row, 0, item_name)
            
            # Category
            item_cat = QTableWidgetItem(info.get('category', 'Other'))
            self.strudel_table.setItem(row, 1, item_cat)
            
            # Size
            item_size = QTableWidgetItem(info.get('size_estimate', 'Unknown'))
            self.strudel_table.setItem(row, 2, item_size)
            
            # Status
            if is_installed:
                status_item = QTableWidgetItem("✅ Installed")
                status_item.setForeground(QColor("#44cc44"))
            else:
                status_item = QTableWidgetItem("Not installed")
                status_item.setForeground(QColor("#808090"))
            self.strudel_table.setItem(row, 3, status_item)
            
            # Action button
            if is_installed:
                btn = QPushButton("✓ Installed")
                btn.setEnabled(False)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #44aa44;
                        border: none;
                        border-radius: 5px;
                        padding: 6px 12px;
                        color: white;
                    }
                """)
            else:
                btn = QPushButton("⬇ Download")
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #648cff;
                        border: none;
                        border-radius: 5px;
                        padding: 6px 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #7499ff;
                    }
                """)
                btn.setToolTip(f"Download {info['display_name']}\n{info['size_estimate']}\n{info['description']}")
                btn.clicked.connect(lambda checked, k=key: self.download_strudel_samples(k))
            
            self.strudel_table.setCellWidget(row, 4, btn)
    
    def download_strudel_samples(self, pack_key: str):
        """Download a Strudel sample pack."""
        from pathlib import Path
        
        try:
            from strudel.sample_catalog import STRUDEL_SAMPLE_CATALOG
        except ImportError:
            QMessageBox.warning(self, "Error", "Sample catalog not found")
            return
        
        if pack_key not in STRUDEL_SAMPLE_CATALOG:
            QMessageBox.warning(self, "Error", f"Unknown sample pack: {pack_key}")
            return
        
        pack_info = STRUDEL_SAMPLE_CATALOG[pack_key]
        display_name = pack_info['display_name']
        
        self.progress_group.setVisible(True)
        self.progress_label.setText(f"⬇️ Downloading {display_name}... ({pack_info['size_estimate']})")
        
        # Download in background
        from ui.workers import StrudelSampleDownloadWorker
        
        samples_dir = Path(__file__).parent.parent.parent.parent / "strudel_samples"
        
        self.sample_download_worker = StrudelSampleDownloadWorker(pack_key, pack_info, samples_dir)
        self.sample_download_worker.finished.connect(lambda success: self.sample_download_finished(success, display_name))
        self.sample_download_worker.status.connect(self.update_status)
        self.sample_download_worker.start()
    
    def sample_download_finished(self, success, message):
        """Handle sample pack download completion."""
        self.progress_group.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Download Complete", f"✅ Successfully downloaded {message}!")
            self.load_strudel_samples()  # Refresh the list
        else:
            QMessageBox.warning(self, "Download Failed", f"❌ Failed to download sample pack:\n{message}")

    def refresh_all(self):
        self.load_installed()
        self.load_catalog()

    def load_installed(self):
        try:
            from utils.cache import get_cached_models, get_total_cache_size
            
            models = get_cached_models()
            total_bytes, total_human = get_total_cache_size()
            
            self.size_label.setText(f"💾 Total: {total_human} ({len(models)} models installed)")
            
            self.installed_table.setRowCount(len(models))
            self.installed_models = models  # Store for delete logic
            
            for i, model in enumerate(models):
                # Try to find display name
                model_key = self._find_model_key(model['name'])
                if model_key and model_key in MODEL_CATALOG:
                    display_name = MODEL_CATALOG[model_key]['display_name']
                    family = MODEL_CATALOG[model_key]['family']
                    desc = MODEL_CATALOG[model_key]['description']
                else:
                    display_name = model['name']
                    family = "Unknown"
                    desc = f"Cached model: {model['name']}"
                
                # Model Name
                item_name = QTableWidgetItem(display_name)
                item_name.setToolTip(desc)
                self.installed_table.setItem(i, 0, item_name)
                
                # Family
                item_family = QTableWidgetItem(family)
                self.installed_table.setItem(i, 1, item_family)
                
                # Size
                item_size = QTableWidgetItem(model['size_human'])
                self.installed_table.setItem(i, 2, item_size)
                
                # Last Accessed
                if model['last_accessed']:
                    accessed = model['last_accessed'].strftime("%Y-%m-%d %H:%M")
                else:
                    accessed = "Unknown"
                item_accessed = QTableWidgetItem(accessed)
                self.installed_table.setItem(i, 3, item_accessed)
                
                # Status
                if model.get('valid', True):
                    status_item = QTableWidgetItem("✅ Ready")
                    status_item.setForeground(QColor("#44cc44"))
                else:
                    status_item = QTableWidgetItem("⚠️ Corrupt/Empty")
                    status_item.setForeground(QColor("#cc4444"))
                    status_item.setToolTip("Model files are missing or incomplete. Try deleting and re-downloading.")
                self.installed_table.setItem(i, 4, status_item)
                
        except Exception as e:
            self.size_label.setText(f"❌ Error loading cache: {e}")
            self.installed_models = []

    def _find_model_key(self, model_name: str) -> str:
        """Find the MODEL_CATALOG key from a cached model name."""
        model_name = model_name.lower()
        for key, info in MODEL_CATALOG.items():
            if info['id'].lower() in model_name or key in model_name:
                return key
        return None

    def load_catalog(self):
        """Load the model catalog with proper display names."""
        from utils.cache import get_cached_models
        
        # Get installed models to mark them
        installed = get_cached_models()
        installed_ids = [m['name'].lower() for m in installed]
        
        # Reset row counts
        for table in self.engine_tables.values():
            table.setRowCount(0)
            
        # Group models by family
        models_by_family = {
            'MusicGen': [],
            'AudioGen': [],
            'MAGNeT': [],
            'ACESTEP': [],
            'DIFFRHYTHM': []
        }
        
        for key, info in MODEL_CATALOG.items():
            family = info['family']
            if family in models_by_family:
                models_by_family[family].append((key, info))
                
        # Populate tables
        for family, models in models_by_family.items():
            if family not in self.engine_tables:
                continue
                
            table = self.engine_tables[family]
            table.setRowCount(len(models))
            
            for row, (key, info) in enumerate(models):
                # Check if installed
                is_installed = any(info['id'].lower() in name for name in installed_ids)
                
                # Features list
                features = []
                if info['stereo']: features.append("🔊 Stereo")
                if info['melody']: features.append("🎵 Melody")
                feature_str = ", ".join(features) if features else "Mono"
                
                # Create items
                item_name = QTableWidgetItem(info['display_name'])
                item_name.setToolTip(info['description'])
                
                item_params = QTableWidgetItem(info['params'])
                item_vram = QTableWidgetItem(f"{info['vram_gb']} GB")
                item_download = QTableWidgetItem(info['download_size'])
                item_quality = QTableWidgetItem(info['quality'])
                item_speed = QTableWidgetItem(info['speed'])
                item_features = QTableWidgetItem(feature_str)
                
                # Set tooltips
                for item in [item_params, item_vram, item_download, item_quality, item_speed, item_features]:
                    item.setToolTip(info['description'])
                
                table.setItem(row, 0, item_name)
                table.setItem(row, 1, item_params)
                table.setItem(row, 2, item_vram)
                table.setItem(row, 3, item_download)
                table.setItem(row, 4, item_quality)
                table.setItem(row, 5, item_speed)
                table.setItem(row, 6, item_features)
                
                # Action Button
                if is_installed:
                    btn = QPushButton("✓ Installed")
                    btn.setEnabled(False)
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #44aa44;
                            border: none;
                            border-radius: 5px;
                            padding: 6px 12px;
                            color: white;
                        }
                    """)
                else:
                    btn = QPushButton(f"⬇ Download")
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #648cff;
                            border: none;
                            border-radius: 5px;
                            padding: 6px 12px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #7499ff;
                        }
                    """)
                    btn.setToolTip(f"Download {info['display_name']}\n{info['download_size']}\n{info['description']}")
                    btn.clicked.connect(lambda checked, n=key: self.start_download(n))
                
                table.setCellWidget(row, 7, btn)

    def delete_selected(self):
        selected = self.installed_table.selectedItems()
        if not selected:
            QMessageBox.information(self, "Info", "No model selected.")
            return
        
        row = selected[0].row()
        if row >= len(self.installed_models):
            return
            
        model = self.installed_models[row]
        
        # Find display name
        model_key = self._find_model_key(model['name'])
        display_name = MODEL_CATALOG.get(model_key, {}).get('display_name', model['name']) if model_key else model['name']
        
        reply = QMessageBox.question(
            self, 
            "Confirm Delete",
            f"Delete {display_name}?\n\nThis will free {model['size_human']} of disk space.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            from utils.cache import delete_model_by_path
            success = delete_model_by_path(model['path'])
            if success:
                QMessageBox.information(self, "Deleted", f"Successfully deleted {display_name}")
                self.refresh_all()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete model.")

    def start_download(self, model_key: str):
        """Start downloading a model."""
        if model_key not in MODEL_CATALOG:
            QMessageBox.warning(self, "Error", f"Unknown model: {model_key}")
            return
        
        model_info = MODEL_CATALOG[model_key]
        family = model_info.get('family', 'MusicGen')
        display_name = model_info['display_name']
        
        self.progress_group.setVisible(True)
        self.progress_label.setText(f"⬇️ Downloading {display_name}... ({model_info['download_size']})")
        
        # Import and run download in background
        from ui.workers import ModelDownloadWorker
        
        loader = None
        
        try:
            if family in ['MusicGen', 'AudioGen', 'MAGNeT']:
                from models.musicgen import MusicGenLoader
                loader = MusicGenLoader(None)
            elif family == 'ACESTEP':
                from models.ace_step import ACEStepLoader
                loader = ACEStepLoader()
            elif family == 'DIFFRHYTHM':
                from models.diffrhythm import DiffRhythmLoader
                loader = DiffRhythmLoader()
            else:
                QMessageBox.warning(self, "Error", f"Unknown model family: {family}")
                self.progress_group.setVisible(False)
                return
                
            self.download_worker = ModelDownloadWorker(loader, model_key)
            self.download_worker.finished.connect(lambda success: self.download_finished(success, display_name))
            
            # Connect status updates
            self.download_worker.status.connect(self.update_status)
            
            self.download_worker.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Install Error", f"Failed to initialize loader for {family}.\n\nError: {e}")
            self.progress_group.setVisible(False)
    
    def update_status(self, msg):
        self.progress_label.setText(msg)
    
    def download_finished(self, success, message):
        self.progress_group.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Download Complete", f"✅ Successfully downloaded {message}!")
            self.refresh_all()
        else:
            QMessageBox.warning(self, "Download Failed", f"❌ Failed to download model:\n{message}")
