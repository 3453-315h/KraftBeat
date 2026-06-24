"""Settings Panel for Kraftbeat."""

import logging
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QPushButton, QLabel, QSpinBox, QComboBox, QCheckBox, QLineEdit,
    QTabWidget, QMessageBox, QWidget as QWidgetBase, QFrame
)
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


class SettingsPanel(QWidget):
    """Application settings panel."""
    
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        from utils.config import ConfigManager
        self.settings = settings or ConfigManager.instance().get_all()
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("⚙️ Settings")
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Tab widget
        tabs = QTabWidget()
        
        # General tab
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "General")
        
        # Audio tab
        audio_tab = self.create_audio_tab()
        tabs.addTab(audio_tab, "Audio")
        
        # Solutions tab (formerly Compute)
        compute_tab = self.create_compute_tab()
        tabs.addTab(compute_tab, "Quantization")
        
        # GPU Backend tabs
        directml_tab = self.create_directml_tab()
        tabs.addTab(directml_tab, "DirectML")
        
        cuda_tab = self.create_cuda_tab()
        tabs.addTab(cuda_tab, "CUDA")
        
        rocm_tab = self.create_rocm_tab()
        tabs.addTab(rocm_tab, "ROCm")
        
        # Performance tab
        perf_tab = self.create_performance_tab()
        tabs.addTab(perf_tab, "Performance")
        
        # Phases tab (Dynamic Structure Engine)
        phases_tab = self.create_phases_tab()
        tabs.addTab(phases_tab, "🎼 Phases")
        
        # About tab
        about_tab = self.create_about_tab()
        tabs.addTab(about_tab, "About")
        
        # Set initial tab
        if 'initial_tab' in self.settings:
            tabs.setCurrentIndex(self.settings['initial_tab'])
            
        layout.addWidget(tabs)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton("💾 Apply Settings")
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def create_general_tab(self):
        widget = QWidgetBase()
        layout = QVBoxLayout(widget)
        
        # Output settings
        output_group = QGroupBox("Output")
        form = QFormLayout(output_group)
        
        self.output_dir = QLineEdit()
        self.output_dir.setPlaceholderText("outputs/")
        form.addRow("Output Directory:", self.output_dir)
        
        self.auto_save = QCheckBox("Auto-save generated audio")
        self.auto_save.setChecked(True)
        form.addRow("", self.auto_save)
        
        layout.addWidget(output_group)
        
        # UI settings
        ui_group = QGroupBox("Interface")
        form2 = QFormLayout(ui_group)
        
        self.show_tooltips = QCheckBox("Show tooltips")
        self.show_tooltips.setChecked(True)
        form2.addRow("", self.show_tooltips)
        
        layout.addWidget(ui_group)
        layout.addStretch()
        
        return widget
    
    def create_audio_tab(self):
        widget = QWidgetBase()
        layout = QVBoxLayout(widget)
        
        # Default generation settings
        gen_group = QGroupBox("Default Generation")
        form = QFormLayout(gen_group)
        
        self.default_duration = QSpinBox()
        self.default_duration.setRange(5, 300)
        self.default_duration.setValue(30)
        self.default_duration.setSuffix(" seconds")
        form.addRow("Duration:", self.default_duration)
        
        self.default_model = QComboBox()
        self.default_model.addItems(["small", "medium", "melody", "large"])
        form.addRow("Default Model:", self.default_model)
        
        layout.addWidget(gen_group)
        
        # Export settings
        export_group = QGroupBox("Export Defaults")
        form2 = QFormLayout(export_group)
        
        self.default_format = QComboBox()
        self.default_format.addItems(["WAV", "MP3", "FLAC", "OGG"])
        form2.addRow("Format:", self.default_format)
        
        self.default_bitrate = QComboBox()
        self.default_bitrate.addItems(["128k", "192k", "256k", "320k"])
        self.default_bitrate.setCurrentText("192k")
        form2.addRow("Bitrate:", self.default_bitrate)
        
        layout.addWidget(export_group)
        
        # Structure Mode (Infinite Generation)
        structure_group = QGroupBox("🎼 Infinite Generation Structure")
        structure_layout = QVBoxLayout(structure_group)
        
        struct_info = QLabel(
            "<b>Structure Mode</b> controls chunk duration for long generations (>30s).<br>"
            "Shorter chunks = tighter coherence, more phases. Uses Fibonacci numbers."
        )
        struct_info.setWordWrap(True)
        struct_info.setStyleSheet("color: #a0a0b0; margin-bottom: 8px;")
        structure_layout.addWidget(struct_info)
        
        struct_form = QFormLayout()
        
        self.structure_mode = QComboBox()
        self.structure_mode.addItems([
            "🎯 Coherent (8s chunks) - Max Control",
            "⚖️ Balanced (13s chunks) - Recommended",
            "⚡ Speed (21s chunks) - Fast Generation"
        ])
        self.structure_mode.setCurrentIndex(1)  # Default to Balanced
        self.structure_mode.setToolTip(
            "Chunk duration affects generation structure:\n"
            "• Coherent: Tightest control, most phases, slowest\n"
            "• Balanced: Good coherence + speed (Fibonacci: 13s)\n"
            "• Speed: Fastest, fewer phases, more creative freedom"
        )
        struct_form.addRow("Mode:", self.structure_mode)
        
        structure_layout.addLayout(struct_form)
        
        # Phase info table
        phase_table = QLabel(
            "<table style='color: #909090; font-size: 11px;'>"
            "<tr><td><b>Coherent:</b></td><td>150s → ~20 chunks</td><td>Very tight structure</td></tr>"
            "<tr><td><b>Balanced:</b></td><td>150s → ~14 chunks</td><td>Good Verse/Chorus flow</td></tr>"
            "<tr><td><b>Speed:</b></td><td>150s → ~8 chunks</td><td>Fast, less repetition</td></tr>"
            "</table>"
        )
        phase_table.setStyleSheet("margin-top: 5px;")
        structure_layout.addWidget(phase_table)
        
        layout.addWidget(structure_group)
        layout.addStretch()
        
        return widget
        
    def create_compute_tab(self):
        """Create the Solutions / Compute settings tab."""
        widget = QWidgetBase()
        layout = QVBoxLayout(widget)
        
        # QUANTIZATION SOLUTION (Highlighted)
        quant_group = QGroupBox("🔧 Quantization (Memory Reduction)")
        quant_group.setStyleSheet("QGroupBox { font-weight: bold; color: #648cff; border: 2px solid #648cff; margin-top: 10px; padding: 10px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 10px; }")
        quant_layout = QVBoxLayout(quant_group)
        
        info_label = QLabel(
            "<b>Running out of VRAM?</b> Quantization reduces model precision to save memory.<br>"
            "Lower bits = less VRAM but slightly lower quality."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #a0a0b0; margin-bottom: 10px;")
        quant_layout.addWidget(info_label)
        
        # Quantization mode selection
        quant_form = QFormLayout()
        
        self.quant_mode = QComboBox()
        self.quant_mode.addItems([
            "None (Full Precision - FP32)",
            "FP16 (Half Precision - 50% less VRAM)",
            "8-bit (INT8 - 75% less VRAM, Recommended)",
            "4-bit (INT4 - 87% less VRAM, Experimental)"
        ])
        self.quant_mode.setCurrentIndex(2)  # Default to 8-bit
        self.quant_mode.setToolTip("Select quantization level. 8-bit recommended for most GPUs.")
        quant_form.addRow("Precision Mode:", self.quant_mode)
        
        # Legacy checkbox for compatibility
        self.use_8bit = QCheckBox("Quick Enable: 8-bit Quantization")
        self.use_8bit.setStyleSheet("font-weight: bold;")
        self.use_8bit.setToolTip("Shortcut to enable 8-bit mode. Same as selecting '8-bit' above.")
        self.use_8bit.stateChanged.connect(lambda state: self.quant_mode.setCurrentIndex(2) if state else None)
        quant_form.addRow("", self.use_8bit)
        
        quant_layout.addLayout(quant_form)
        
        # VRAM savings estimate
        vram_label = QLabel(
            "<table style='color: #909090; font-size: 11px;'>"
            "<tr><td><b>FP32:</b></td><td>~8-18 GB</td><td style='color:#ff6060;'>❌ Large models may crash</td></tr>"
            "<tr><td><b>FP16:</b></td><td>~4-9 GB</td><td style='color:#ffcc00;'>⚠️ Good for 8GB+ VRAM</td></tr>"
            "<tr><td><b>INT8:</b></td><td>~2-5 GB</td><td style='color:#60ff60;'>✅ Recommended</td></tr>"
            "<tr><td><b>INT4:</b></td><td>~1-3 GB</td><td style='color:#6090ff;'>🔬 Experimental</td></tr>"
            "</table>"
        )
        vram_label.setStyleSheet("margin-top: 8px;")
        quant_layout.addWidget(vram_label)
        
        layout.addWidget(quant_group)

        # GPU / Backend settings
        gpu_group = QGroupBox("Compute Device Backend")
        form = QFormLayout(gpu_group)
        
        self.device_combo = QComboBox()
        self.device_combo.addItems(["Auto", "DirectML (AMD/Intel)", "CUDA (NVIDIA)", "ROCm (AMD Native)", "ZLUDA (AMD->CUDA)", "CPU"])
        self.device_combo.setToolTip("Select compute backend. 'Auto' detects the best option.")
        form.addRow("Backend:", self.device_combo)
        
        self.device_index = QSpinBox()
        self.device_index.setRange(0, 7)
        self.device_index.setValue(0)
        self.device_index.setToolTip("GPU index if you have multiple GPUs (0 = first)")
        form.addRow("GPU Index:", self.device_index)
        
        layout.addWidget(gpu_group)
        
        # VRAM Management
        mem_group = QGroupBox("VRAM Management")
        mem_form = QFormLayout(mem_group)
        
        self.offload_cpu = QCheckBox("Offload to CPU when idle")
        self.offload_cpu.setToolTip("Move model to CPU RAM when not generating to free VRAM")
        mem_form.addRow("", self.offload_cpu)
        
        self.clear_cache_on_exit = QCheckBox("Clear VRAM cache on exit")
        self.clear_cache_on_exit.setChecked(True)
        mem_form.addRow("", self.clear_cache_on_exit)
        
        self.aggressive_gc = QCheckBox("Aggressive garbage collection")
        self.aggressive_gc.setToolTip("Run gc.collect() more frequently to reclaim memory")
        mem_form.addRow("", self.aggressive_gc)
        
        self.max_vram = QSpinBox()
        self.max_vram.setRange(0, 48)
        self.max_vram.setValue(0)
        self.max_vram.setSuffix(" GB")
        self.max_vram.setToolTip("Limit VRAM usage (0 = no limit)")
        self.max_vram.setSpecialValueText("No limit")
        mem_form.addRow("Max VRAM:", self.max_vram)
        
        layout.addWidget(mem_group)
        
        # Model Loading Options
        load_group = QGroupBox("Model Loading")
        load_form = QFormLayout(load_group)
        
        self.use_flash_attn = QCheckBox("Use Flash Attention (if available)")
        self.use_flash_attn.setChecked(True)
        self.use_flash_attn.setToolTip("Faster attention computation with less memory. Requires compatible GPU.")
        load_form.addRow("", self.use_flash_attn)
        
        self.use_compile = QCheckBox("Use torch.compile() optimization")
        self.use_compile.setToolTip("JIT compile model for faster inference. Increases startup time.")
        load_form.addRow("", self.use_compile)
        
        self.use_bettertransformer = QCheckBox("Use BetterTransformer")
        self.use_bettertransformer.setChecked(True)
        self.use_bettertransformer.setToolTip("Optimized attention implementation from optimum library")
        load_form.addRow("", self.use_bettertransformer)
        
        layout.addWidget(load_group)
        layout.addStretch()
        
        return widget
    
    def create_directml_tab(self):
        """Create DirectML settings tab (AMD/Intel on Windows)."""
        widget = QWidgetBase()
        layout = QVBoxLayout(widget)
        
        # Info header
        info_group = QGroupBox("DirectML (AMD/Intel Windows)")
        info_layout = QVBoxLayout(info_group)
        
        info_label = QLabel(
            "<b>DirectML</b> is the default backend for AMD and Intel GPUs on Windows.<br><br>"
            "<b>Supported:</b> AMD RX 400+ series, Intel Arc, Intel UHD<br>"
            "<b>Status:</b> Stable, recommended for most AMD/Intel users"
        )
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        layout.addWidget(info_group)
        
        # Settings
        settings_group = QGroupBox("DirectML Options")
        form = QFormLayout(settings_group)
        
        self.dml_device_index = QSpinBox()
        self.dml_device_index.setRange(0, 7)
        self.dml_device_index.setValue(0)
        self.dml_device_index.setToolTip("GPU index if multiple GPUs installed (0 = first GPU)")
        form.addRow("GPU Index:", self.dml_device_index)
        
        self.dml_fallback_cpu = QCheckBox("Fallback to CPU if DirectML fails")
        self.dml_fallback_cpu.setChecked(True)
        form.addRow("", self.dml_fallback_cpu)
        
        layout.addWidget(settings_group)
        
        # Install info
        install_group = QGroupBox("Installation")
        install_layout = QVBoxLayout(install_group)
        install_label = QLabel(
            "<code>pip install torch-directml</code><br><br>"
            "DirectML comes pre-installed with Kraftbeat."
        )
        install_label.setWordWrap(True)
        install_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        install_layout.addWidget(install_label)
        layout.addWidget(install_group)
        
        layout.addStretch()
        return widget
    
    def create_cuda_tab(self):
        """Create CUDA settings tab (NVIDIA)."""
        widget = QWidgetBase()
        layout = QVBoxLayout(widget)
        
        # Info header
        info_group = QGroupBox("CUDA (NVIDIA GPUs)")
        info_layout = QVBoxLayout(info_group)
        
        info_label = QLabel(
            "<b>CUDA</b> is NVIDIA's GPU computing platform.<br><br>"
            "<b>Supported:</b> GTX 900+, RTX series, Quadro, Tesla<br>"
            "<b>Status:</b> Best performance, full feature support"
        )
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        layout.addWidget(info_group)
        
        # Settings
        settings_group = QGroupBox("CUDA Options")
        form = QFormLayout(settings_group)
        
        self.cuda_device_id = QSpinBox()
        self.cuda_device_id.setRange(0, 7)
        self.cuda_device_id.setValue(0)
        self.cuda_device_id.setToolTip("CUDA device ID (0 = first GPU)")
        form.addRow("Device ID:", self.cuda_device_id)
        
        self.cuda_fp16 = QCheckBox("Use FP16 (Half Precision)")
        self.cuda_fp16.setToolTip("Faster inference, slightly lower quality. Recommended for RTX cards.")
        form.addRow("", self.cuda_fp16)
        
        self.cuda_flash_attn = QCheckBox("Enable Flash Attention (if available)")
        self.cuda_flash_attn.setChecked(True)
        self.cuda_flash_attn.setToolTip("Faster attention computation. Requires xformers or flash-attn.")
        form.addRow("", self.cuda_flash_attn)
        
        self.cuda_compile = QCheckBox("Use torch.compile() optimization")
        self.cuda_compile.setToolTip("JIT compilation for faster inference. May increase startup time.")
        form.addRow("", self.cuda_compile)
        
        layout.addWidget(settings_group)
        
        # Install info
        install_group = QGroupBox("Installation")
        install_layout = QVBoxLayout(install_group)
        install_label = QLabel(
            "<code>pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121</code><br><br>"
            "<b>Optional:</b> <code>pip install xformers flash-attn</code> for faster attention"
        )
        install_label.setWordWrap(True)
        install_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        install_layout.addWidget(install_label)
        layout.addWidget(install_group)
        
        layout.addStretch()
        return widget
    
    def create_rocm_tab(self):
        """Create ROCm settings tab (AMD Native)."""
        widget = QWidgetBase()
        layout = QVBoxLayout(widget)
        
        # Info header
        info_group = QGroupBox("ROCm (AMD Native)")
        info_layout = QVBoxLayout(info_group)
        
        info_label = QLabel(
            "<b>ROCm</b> is AMD's native GPU computing platform.<br><br>"
            "<b>Supported (Windows Preview):</b> RX 7000/9000 series, Ryzen AI APUs<br>"
            "<b>Supported (Linux):</b> RX 5000+, Instinct MI series<br>"
            "<b>Status:</b> Windows support in preview, Linux stable"
        )
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        layout.addWidget(info_group)
        
        # Settings
        settings_group = QGroupBox("ROCm Options")
        form = QFormLayout(settings_group)
        
        self.rocm_device_id = QSpinBox()
        self.rocm_device_id.setRange(0, 7)
        self.rocm_device_id.setValue(0)
        self.rocm_device_id.setToolTip("HIP device ID (0 = first GPU)")
        form.addRow("Device ID:", self.rocm_device_id)
        
        self.rocm_hip_visible = QLineEdit()
        self.rocm_hip_visible.setPlaceholderText("0,1 (leave empty for all)")
        self.rocm_hip_visible.setToolTip("Set HIP_VISIBLE_DEVICES environment variable")
        form.addRow("Visible Devices:", self.rocm_hip_visible)
        
        self.rocm_flash_attn = QCheckBox("Enable Triton Flash Attention")
        self.rocm_flash_attn.setToolTip("ROCm's Flash Attention via Triton (PyTorch 2.5+)")
        form.addRow("", self.rocm_flash_attn)
        
        self.rocm_sdpa = QCheckBox("Use Scaled Dot Product Attention")
        self.rocm_sdpa.setChecked(True)
        self.rocm_sdpa.setToolTip("PyTorch's optimized attention, auto-selects best backend")
        form.addRow("", self.rocm_sdpa)
        
        layout.addWidget(settings_group)
        
        # Install info
        install_group = QGroupBox("Installation (Windows)")
        install_layout = QVBoxLayout(install_group)
        install_label = QLabel(
            "<b>1.</b> Install AMD PyTorch Preview Driver from AMD.com<br>"
            "<b>2.</b> <code>pip install -r requirements/rocm.txt</code><br><br>"
            "<b>Requirements:</b> Windows 11, RX 7000/9000 or Ryzen AI APU"
        )
        install_label.setWordWrap(True)
        install_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        install_layout.addWidget(install_label)
        layout.addWidget(install_group)
        
        # Linux install info
        linux_group = QGroupBox("Installation (Linux)")
        linux_layout = QVBoxLayout(linux_group)
        linux_label = QLabel(
            "<code>pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2</code>"
        )
        linux_label.setWordWrap(True)
        linux_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        linux_layout.addWidget(linux_label)
        layout.addWidget(linux_group)
        
        layout.addStretch()
        return widget
    
    def create_performance_tab(self):
        """Create Performance tab with threading, pooling, and optimization settings."""
        widget = QWidgetBase()
        layout = QVBoxLayout(widget)
        
        # Threading Settings
        thread_group = QGroupBox("Multithreading")
        thread_form = QFormLayout(thread_group)
        
        # Number of worker threads
        cpu_count = os.cpu_count() or 4
        self.num_workers = QSpinBox()
        self.num_workers.setRange(1, cpu_count * 2)
        self.num_workers.setValue(min(4, cpu_count))
        self.num_workers.setToolTip(f"Number of parallel worker threads (CPU cores: {cpu_count})")
        thread_form.addRow("Worker Threads:", self.num_workers)
        
        # Thread pool size for background tasks
        self.pool_size = QSpinBox()
        self.pool_size.setRange(1, 16)
        self.pool_size.setValue(4)
        self.pool_size.setToolTip("Size of thread pool for background tasks (audio processing, effects)")
        thread_form.addRow("Thread Pool Size:", self.pool_size)
        
        # PyTorch threads
        self.torch_threads = QSpinBox()
        self.torch_threads.setRange(1, cpu_count)
        self.torch_threads.setValue(min(4, cpu_count))
        self.torch_threads.setToolTip("Number of threads for PyTorch CPU operations (torch.set_num_threads)")
        thread_form.addRow("PyTorch Threads:", self.torch_threads)
        
        layout.addWidget(thread_group)
        
        # Batch Processing
        batch_group = QGroupBox("Batch Processing")
        batch_form = QFormLayout(batch_group)
        
        self.batch_size = QSpinBox()
        self.batch_size.setRange(1, 8)
        self.batch_size.setValue(1)
        self.batch_size.setToolTip("Batch size for variation generation (higher = more VRAM, faster)")
        batch_form.addRow("Variation Batch Size:", self.batch_size)
        
        self.parallel_effects = QCheckBox("Parallel effects processing")
        self.parallel_effects.setChecked(True)
        self.parallel_effects.setToolTip("Process audio effects in parallel using thread pool")
        batch_form.addRow("", self.parallel_effects)
        
        self.async_save = QCheckBox("Async file saving")
        self.async_save.setChecked(True)
        self.async_save.setToolTip("Save audio files in background without blocking UI")
        batch_form.addRow("", self.async_save)
        
        layout.addWidget(batch_group)
        
        # Memory Optimization
        mem_group = QGroupBox("Memory Optimization")
        mem_form = QFormLayout(mem_group)
        
        self.lazy_loading = QCheckBox("Lazy model loading")
        self.lazy_loading.setToolTip("Only load models when needed, unload after inactivity")
        self.lazy_loading.setChecked(True)
        mem_form.addRow("", self.lazy_loading)
        
        self.model_unload_timeout = QSpinBox()
        self.model_unload_timeout.setRange(0, 60)
        self.model_unload_timeout.setValue(10)
        self.model_unload_timeout.setSuffix(" min")
        self.model_unload_timeout.setToolTip("Unload model after inactivity (0 = never)")
        mem_form.addRow("Unload After:", self.model_unload_timeout)
        
        self.gc_on_generate = QCheckBox("Force garbage collection after generation")
        self.gc_on_generate.setChecked(False)
        self.gc_on_generate.setToolTip("Run gc.collect() after each generation to free memory")
        mem_form.addRow("", self.gc_on_generate)
        
        self.clear_cache_between = QCheckBox("Clear CUDA/DirectML cache between generations")
        self.clear_cache_between.setChecked(False)
        self.clear_cache_between.setToolTip("May help with VRAM fragmentation but slower")
        mem_form.addRow("", self.clear_cache_between)
        
        layout.addWidget(mem_group)
        
        # Apply button for threading settings
        apply_info = QLabel(
            "<i>Threading changes take effect on next generation. "
            "Restart app for PyTorch thread count.</i>"
        )
        apply_info.setWordWrap(True)
        apply_info.setStyleSheet("color: #808090; font-size: 11px; margin-top: 10px;")
        layout.addWidget(apply_info)
        
        layout.addStretch()
        
        return widget
    
    def create_phases_tab(self):
        """Create the Phases tab for editing Dynamic Structure Engine phase modifiers."""
        import json
        from pathlib import Path
        from PyQt6.QtWidgets import QScrollArea
        
        # Main widget with scroll
        main_widget = QWidgetBase()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # Content widget inside scroll
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Header
        header_label = QLabel(
            "<b>🎼 Phase Modifiers</b><br>"
            "<span style='color: #a0a0b0;'>Define the musical phases for structured generation. "
            "These phases are mapped to chunks using <b>golden ratio positioning</b> (φ = 0.618).</span><br><br>"
            "<span style='color: #ff9060;'>💡 Tip: Use Fibonacci numbers (8, 13, 21) for optimal phase counts.</span>"
        )
        header_label.setWordWrap(True)
        layout.addWidget(header_label)
        
        # Load phases from JSON
        phases_file = Path(__file__).parent.parent.parent.parent / "config" / "phases.json"
        self.phases_data = {}
        self.phases_file_path = phases_file
        
        try:
            if phases_file.exists():
                with open(phases_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.phases_data = data.get('phases', {})
                    self.phases_presets = data.get('presets', {})
        except Exception as e:
            logger.error(f"Failed to load phases.json: {e}")
            self.phases_data = {}
            self.phases_presets = {}
        
        # Golden Ratio Info
        ratio_info = QLabel(
            "<table style='color: #909090; font-size: 11px;'>"
            "<tr><td><b>Golden Ratio Mapping:</b></td></tr>"
            "<tr><td>• Intro → 0-15% of chunks</td></tr>"
            "<tr><td>• Verse/Chorus → 15-55%</td></tr>"
            "<tr><td>• <span style='color: #ffcc00;'>Bridge/Peak → ~61.8% (φ)</span></td></tr>"
            "<tr><td>• Climax/Outro → 62-100%</td></tr>"
            "</table>"
        )
        layout.addWidget(ratio_info)
        
        # Phase Count Selector
        count_group = QGroupBox("Phase Count")
        count_layout = QHBoxLayout(count_group)
        
        count_label = QLabel("Number of Phases:")
        count_layout.addWidget(count_label)
        
        self.phase_count_combo = QComboBox()
        self.phase_count_combo.addItems([
            "8 Phases (Speed)",
            "10 Phases (Default)",
            "13 Phases (Balanced)",
            "21 Phases (Coherent)"
        ])
        self.phase_count_combo.setCurrentIndex(1)  # Default to 10
        self.phase_count_combo.currentIndexChanged.connect(self._load_phase_count)
        self.phase_count_combo.setToolTip(
            "8 = Speed mode, fewer phases\n"
            "10 = Default, balanced phases\n"
            "13 = Fibonacci, detailed structure\n"
            "21 = Maximum control, granular phases"
        )
        count_layout.addWidget(self.phase_count_combo)
        
        count_layout.addStretch()
        layout.addWidget(count_group)
        
        # Preset selector (genre presets)
        preset_group = QGroupBox("Genre Presets")
        preset_layout = QHBoxLayout(preset_group)
        
        preset_label = QLabel("Load Preset:")
        preset_layout.addWidget(preset_label)
        
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(["Default", "EDM", "Jazz", "Ambient"])
        self.preset_combo.currentTextChanged.connect(self._load_phase_preset)
        preset_layout.addWidget(self.preset_combo)
        
        preset_layout.addStretch()
        layout.addWidget(preset_group)
        
        # Phase editors - count phases dynamically
        phase_count = len(self.phases_data) if self.phases_data else 10
        phases_group = QGroupBox(f"Phase Modifiers ({phase_count} Phases)")
        phases_form = QFormLayout(phases_group)
        
        # Phase order for display
        phase_order = [
            ("intro", "🎬 Intro"),
            ("verse_early", "📖 Verse (Early)"),
            ("verse_late", "📖 Verse (Late)"),
            ("pre_chorus", "⬆️ Pre-Chorus"),
            ("chorus", "🎵 Chorus"),
            ("chorus_peak", "🎵 Chorus (Peak)"),
            ("bridge", "🌉 Bridge"),
            ("climax", "🔥 Climax"),
            ("outro_early", "🌅 Outro (Early)"),
            ("outro_fade", "🌅 Outro (Fade)")
        ]
        
        self.phase_editors = {}
        
        for phase_key, phase_label in phase_order:
            editor = QLineEdit()
            
            # Handle both old (string) and new (dict) format
            phase_data = self.phases_data.get(phase_key, "")
            if isinstance(phase_data, dict):
                # New format: show base, tooltip shows sub-prompt count
                base_text = phase_data.get('base', '')
                sub_count = len(phase_data.get('sub_prompts', []))
                editor.setText(base_text)
                editor.setToolTip(f"Base: {base_text}\nSub-prompts: {sub_count} variations")
            elif isinstance(phase_data, str):
                editor.setText(phase_data)
            else:
                editor.setText("")
            
            editor.setPlaceholderText(f"Base modifier for {phase_key}...")
            editor.setMinimumWidth(400)
            self.phase_editors[phase_key] = editor
            phases_form.addRow(phase_label + ":", editor)
        
        layout.addWidget(phases_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        reset_btn = QPushButton("🔄 Reset to Defaults")
        reset_btn.clicked.connect(self._reset_phases_to_default)
        btn_layout.addWidget(reset_btn)
        
        save_phases_btn = QPushButton("💾 Save Phases")
        save_phases_btn.setStyleSheet("font-weight: bold;")
        save_phases_btn.clicked.connect(self._save_phases_to_json)
        btn_layout.addWidget(save_phases_btn)
        
        layout.addLayout(btn_layout)
        
        # Info
        info_label = QLabel(
            "<i style='color: #808090;'>Changes are saved to config/phases.json and apply immediately to new generations.</i>"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        # Set content widget to scroll area
        scroll.setWidget(widget)
        main_layout.addWidget(scroll)
        
        return main_widget
    
    def _load_phase_preset(self, preset_name: str):
        """Load a phase preset into the editors."""
        preset_key = preset_name.lower()
        
        if preset_key == "default":
            # Load from original default
            defaults = {
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
            for key, editor in self.phase_editors.items():
                editor.setText(defaults.get(key, ""))
        elif preset_key in self.phases_presets:
            preset = self.phases_presets[preset_key]
            if isinstance(preset, dict):
                for key, editor in self.phase_editors.items():
                    editor.setText(preset.get(key, ""))
    
    def _load_phase_count(self, index: int):
        """Load phases from the appropriate phases_X.json file."""
        import json
        from pathlib import Path
        
        # Map index to phase count
        phase_counts = [8, 10, 13, 21]
        if index < 0 or index >= len(phase_counts):
            return
            
        count = phase_counts[index]
        
        # Build file path
        config_dir = Path(__file__).parent.parent.parent.parent / "config"
        phases_file = config_dir / f"phases_{count}.json"
        
        # Fallback to default phases.json
        if not phases_file.exists():
            phases_file = config_dir / "phases.json"
        
        try:
            if phases_file.exists():
                with open(phases_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.phases_data = data.get('phases', {})
                    self.phases_presets = data.get('presets', {})
                    self.phases_file_path = phases_file
                    
                    # Update editors with new phases
                    for key, editor in self.phase_editors.items():
                        phase_data = self.phases_data.get(key, "")
                        if isinstance(phase_data, dict):
                            editor.setText(phase_data.get('base', ''))
                        elif isinstance(phase_data, str):
                            editor.setText(phase_data)
                        else:
                            editor.setText("")
                    
                    logger.info(f"Loaded {count}-phase configuration from {phases_file}")
        except Exception as e:
            logger.error(f"Failed to load phases_{count}.json: {e}")
    
    def _reset_phases_to_default(self):
        """Reset all phases to default values."""
        self.preset_combo.setCurrentText("Default")
        self._load_phase_preset("Default")
    
    def _save_phases_to_json(self):
        """Save current phase values to JSON file."""
        import json
        
        # Collect current values
        phases = {}
        for key, editor in self.phase_editors.items():
            phases[key] = editor.text()
        
        # Load existing file to preserve presets
        try:
            if self.phases_file_path.exists():
                with open(self.phases_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}
        except Exception as e:
            logger.debug(f"Failed to load existing phases: {e}")
            data = {}
        
        # Update phases
        data['phases'] = phases
        data['version'] = "1.0"
        data['description'] = "Phase modifiers for the Dynamic Structure Engine."
        
        # Save
        try:
            self.phases_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.phases_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            QMessageBox.information(self, "Saved", "Phase modifiers saved successfully!")
            
            # Update internal data
            self.phases_data = phases
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save: {e}")

    def create_about_tab(self):
        """Create the About tab."""
        widget = QWidgetBase()
        layout = QVBoxLayout(widget)
        
        # Title
        title_label = QLabel("Kraftbeat")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #648cff; margin-bottom: 5px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Version
        try:
            from src import __version__
            version_str = f"v{__version__}"
        except ImportError:
            version_str = "v0.1.0"
            
        ver_label = QLabel(version_str)
        ver_label.setStyleSheet("color: #808090; font-size: 14px; margin-bottom: 20px;")
        ver_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ver_label)
        
        # Description
        desc_label = QLabel(
            "AI-powered music generation tool.\n"
            "Powered by Meta's MusicGen and PyTorch."
        )
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Credits group
        credits_group = QGroupBox("Credits")
        form = QFormLayout(credits_group)
        form.addRow("Backend:", QLabel("MusicGen (audiocraft/transformers)"))
        form.addRow("GUI Framework:", QLabel("PyQt6"))
        form.addRow("Audio:", QLabel("SoundFile, SoundDevice"))
        layout.addWidget(credits_group)
        
        # Links
        links_label = QLabel('<a href="https://github.com/facebookresearch/audiocraft">MusicGen Repository</a>')
        links_label.setOpenExternalLinks(True)
        links_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(links_label)
        
        layout.addStretch()
        return widget
    
    def load_settings(self):
        """Load settings into UI."""
        # General tab
        self.output_dir.setText(self.settings.get('output_dir', 'outputs/'))
        self.auto_save.setChecked(self.settings.get('auto_save', True))
        self.show_tooltips.setChecked(self.settings.get('show_tooltips', True))
        
        # Audio tab
        self.default_duration.setValue(self.settings.get('default_duration', 30))
        model_idx = self.default_model.findText(self.settings.get('default_model', 'small'))
        if model_idx >= 0: self.default_model.setCurrentIndex(model_idx)
        format_idx = self.default_format.findText(self.settings.get('default_format', 'WAV'))
        if format_idx >= 0: self.default_format.setCurrentIndex(format_idx)
        bitrate_idx = self.default_bitrate.findText(self.settings.get('default_bitrate', '192k'))
        if bitrate_idx >= 0: self.default_bitrate.setCurrentIndex(bitrate_idx)
        
        structure_map = {'coherent': 0, 'balanced': 1, 'speed': 2}
        struct_idx = structure_map.get(self.settings.get('structure_mode', 'balanced'), 1)
        self.structure_mode.setCurrentIndex(struct_idx)
        
        # Quantization tab
        self.quant_mode.setCurrentIndex(self.settings.get('quant_mode', 2))
        self.use_8bit.setChecked(self.settings.get('use_8bit', False))
        
        device_idx = self.device_combo.findText(self.settings.get('device', 'Auto'))
        if device_idx >= 0: self.device_combo.setCurrentIndex(device_idx)
        self.device_index.setValue(self.settings.get('device_index', 0))
        
        # VRAM Management
        self.offload_cpu.setChecked(self.settings.get('offload_cpu', False))
        self.clear_cache_on_exit.setChecked(self.settings.get('clear_cache_on_exit', True))
        self.aggressive_gc.setChecked(self.settings.get('aggressive_gc', False))
        self.max_vram.setValue(self.settings.get('max_vram', 0))
        
        # Model Loading
        self.use_flash_attn.setChecked(self.settings.get('use_flash_attn', True))
        self.use_compile.setChecked(self.settings.get('use_compile', False))
        self.use_bettertransformer.setChecked(self.settings.get('use_bettertransformer', True))
        
        # DirectML
        self.dml_device_index.setValue(self.settings.get('dml_device_index', 0))
        self.dml_fallback_cpu.setChecked(self.settings.get('dml_fallback_cpu', True))
        
        # CUDA
        self.cuda_device_id.setValue(self.settings.get('cuda_device_id', 0))
        self.cuda_fp16.setChecked(self.settings.get('cuda_fp16', False))
        self.cuda_flash_attn.setChecked(self.settings.get('cuda_flash_attn', True))
        self.cuda_compile.setChecked(self.settings.get('cuda_compile', False))
        
        # ROCm
        self.rocm_device_id.setValue(self.settings.get('rocm_device_id', 0))
        self.rocm_hip_visible.setText(self.settings.get('rocm_hip_visible', ''))
        self.rocm_flash_attn.setChecked(self.settings.get('rocm_flash_attn', False))
        self.rocm_sdpa.setChecked(self.settings.get('rocm_sdpa', True))
        
        # Performance - Threading
        self.num_workers.setValue(self.settings.get('num_workers', 4))
        self.pool_size.setValue(self.settings.get('pool_size', 4))
        self.torch_threads.setValue(self.settings.get('torch_threads', 4))
        
        # Performance - Batch
        self.batch_size.setValue(self.settings.get('batch_size', 1))
        self.parallel_effects.setChecked(self.settings.get('parallel_effects', True))
        self.async_save.setChecked(self.settings.get('async_save', True))
        
        # Performance - Memory
        self.lazy_loading.setChecked(self.settings.get('lazy_loading', True))
        self.model_unload_timeout.setValue(self.settings.get('model_unload_timeout', 10))
        self.gc_on_generate.setChecked(self.settings.get('gc_on_generate', False))
        self.clear_cache_between.setChecked(self.settings.get('clear_cache_between', False))
    
    def save_settings(self):
        """Save settings and apply."""
        self.settings = {
            # General
            'output_dir': self.output_dir.text() or 'outputs/',
            'auto_save': self.auto_save.isChecked(),
            'show_tooltips': self.show_tooltips.isChecked(),
            # Audio
            'default_duration': self.default_duration.value(),
            'default_model': self.default_model.currentText(),
            'default_format': self.default_format.currentText(),
            'default_bitrate': self.default_bitrate.currentText(),
            # Structure Mode (Fibonacci-based chunks)
            'structure_mode': ['coherent', 'balanced', 'speed'][self.structure_mode.currentIndex()],
            # Solutions - Quantization
            'quant_mode': self.quant_mode.currentIndex(),
            'quant_mode_text': self.quant_mode.currentText(),
            'use_8bit': self.use_8bit.isChecked(),
            # Solutions - Device
            'device': self.device_combo.currentText(),
            'device_index': self.device_index.value(),
            # Solutions - VRAM Management
            'offload_cpu': self.offload_cpu.isChecked(),
            'clear_cache_on_exit': self.clear_cache_on_exit.isChecked(),
            'aggressive_gc': self.aggressive_gc.isChecked(),
            'max_vram': self.max_vram.value(),
            # Solutions - Model Loading
            'use_flash_attn': self.use_flash_attn.isChecked(),
            'use_compile': self.use_compile.isChecked(),
            'use_bettertransformer': self.use_bettertransformer.isChecked(),
            # DirectML Tab
            'dml_device_index': self.dml_device_index.value(),
            'dml_fallback_cpu': self.dml_fallback_cpu.isChecked(),
            # CUDA Tab
            'cuda_device_id': self.cuda_device_id.value(),
            'cuda_fp16': self.cuda_fp16.isChecked(),
            'cuda_flash_attn': self.cuda_flash_attn.isChecked(),
            'cuda_compile': self.cuda_compile.isChecked(),
            # ROCm Tab
            'rocm_device_id': self.rocm_device_id.value(),
            'rocm_hip_visible': self.rocm_hip_visible.text(),
            'rocm_flash_attn': self.rocm_flash_attn.isChecked(),
            'rocm_sdpa': self.rocm_sdpa.isChecked(),
            # Performance - Threading
            'num_workers': self.num_workers.value(),
            'pool_size': self.pool_size.value(),
            'torch_threads': self.torch_threads.value(),
            # Performance - Batch
            'batch_size': self.batch_size.value(),
            'parallel_effects': self.parallel_effects.isChecked(),
            'async_save': self.async_save.isChecked(),
            # Performance - Memory
            'lazy_loading': self.lazy_loading.isChecked(),
            'model_unload_timeout': self.model_unload_timeout.value(),
            'gc_on_generate': self.gc_on_generate.isChecked(),
            'clear_cache_between': self.clear_cache_between.isChecked(),
        }
        
        # Apply performance settings
        try:
            from src.utils.performance import update_settings, get_pool
            update_settings(
                num_workers=self.settings['num_workers'],
                pool_size=self.settings['pool_size'],
                torch_threads=self.settings['torch_threads'],
                batch_size=self.settings['batch_size'],
                parallel_effects=self.settings['parallel_effects'],
                async_save=self.settings['async_save'],
                lazy_loading=self.settings['lazy_loading'],
                model_unload_timeout=self.settings['model_unload_timeout'],
                gc_on_generate=self.settings['gc_on_generate'] or self.settings['aggressive_gc'],
                clear_cache_between=self.settings['clear_cache_between'],
            )
            # Restart pool with new size if changed
            get_pool().start(self.settings['pool_size'])
        except Exception as e:
            logger.error(f"Failed to apply performance settings: {e}")
        
        # Apply quantization settings
        try:
            quant_idx = self.settings['quant_mode']
            if quant_idx == 0:  # FP32
                os.environ['KRAFTBEAT_PRECISION'] = 'fp32'
            elif quant_idx == 1:  # FP16
                os.environ['KRAFTBEAT_PRECISION'] = 'fp16'
            elif quant_idx == 2:  # INT8
                os.environ['KRAFTBEAT_PRECISION'] = 'int8'
            elif quant_idx == 3:  # INT4
                os.environ['KRAFTBEAT_PRECISION'] = 'int4'
            
            # Set max VRAM limit
            if self.settings['max_vram'] > 0:
                os.environ['KRAFTBEAT_MAX_VRAM'] = str(self.settings['max_vram'])
            
            # Set device index
            os.environ['KRAFTBEAT_DEVICE_INDEX'] = str(self.settings['device_index'])
            
            # Flash attention flag
            os.environ['KRAFTBEAT_FLASH_ATTN'] = '1' if self.settings['use_flash_attn'] else '0'
            
            # Better transformer flag
            os.environ['KRAFTBEAT_BETTER_TRANSFORMER'] = '1' if self.settings['use_bettertransformer'] else '0'
            
            logger.info(f"Applied: Precision={os.environ.get('KRAFTBEAT_PRECISION', 'auto')}, "
                        f"MaxVRAM={self.settings['max_vram']}GB, FlashAttn={self.settings['use_flash_attn']}")
        except Exception as e:
            logger.error(f"Failed to apply quantization settings: {e}")
            
        # Save to centralized config
        try:
            from utils.config import ConfigManager
            ConfigManager.instance().update(self.settings)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
        
        QMessageBox.information(self, "Settings Saved", "Settings applied successfully!\n\nSome settings require model reload to take effect.")
        
        # Notify parent
        if self.parent():
            # If parent has status bar (MainWindow)
            if hasattr(self.parent(), 'status_bar'):
                self.parent().status_bar.showMessage("Settings saved")
            if hasattr(self.parent(), 'app_settings'):
                 self.parent().app_settings = self.settings
            if hasattr(self.parent(), 'on_settings_updated'):
                 self.parent().on_settings_updated()
    
    def get_settings(self):
        """Return current settings."""
        return self.settings


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Dark theme for test
    app.setStyleSheet("QDialog { background-color: #2b2b35; color: #ffffff; }")
    
    print("Running Settings Panel in standalone debug mode...")
    dlg = SettingsPanel(settings={'theme': 'Dark'})
    dlg.show()
    
    sys.exit(app.exec())
