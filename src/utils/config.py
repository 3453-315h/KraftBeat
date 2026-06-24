"""
Kraftbeat - Centralized Configuration System

Manages loading, saving, and validation of all application settings
stored in config/settings.json.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Find project root (three levels up from src/utils/config.py)
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
SETTINGS_FILE = CONFIG_DIR / "settings.json"

DEFAULT_SETTINGS = {
    # General
    'output_dir': 'outputs/',
    'models_dir': 'models/',
    'auto_save': True,
    'show_tooltips': True,
    # Audio
    'default_duration': 30,
    'default_model': 'small',
    'default_format': 'WAV',
    'default_bitrate': '192k',
    # Structure Mode (coherent, balanced, speed)
    'structure_mode': 'balanced',
    # Solutions - Quantization
    'quant_mode': 2,  # 8-bit
    'quant_mode_text': '8-bit (INT8 - 75% less VRAM, Recommended)',
    'use_8bit': False,
    # Solutions - Device
    'device': 'Auto',
    'device_index': 0,
    # Solutions - VRAM Management
    'offload_cpu': False,
    'clear_cache_on_exit': True,
    'aggressive_gc': False,
    'max_vram': 0,
    # Solutions - Model Loading
    'use_flash_attn': True,
    'use_compile': False,
    'use_bettertransformer': True,
    # DirectML Tab
    'dml_device_index': 0,
    'dml_fallback_cpu': True,
    # CUDA Tab
    'cuda_device_id': 0,
    'cuda_fp16': False,
    'cuda_flash_attn': True,
    'cuda_compile': False,
    # ROCm Tab
    'rocm_device_id': 0,
    'rocm_hip_visible': '',
    'rocm_flash_attn': False,
    'rocm_sdpa': True,
    # Performance - Threading
    'num_workers': 4,
    'pool_size': 4,
    'torch_threads': 4,
    # Performance - Batch
    'batch_size': 1,
    'parallel_effects': True,
    'async_save': True,
    # Performance - Memory
    'lazy_loading': True,
    'model_unload_timeout': 10,
    'gc_on_generate': False,
    'clear_cache_between': False,
    
    # Network config
    'api_host': '127.0.0.1',
    'api_port': 8765,
    'strudel_host': '127.0.0.1',
    
    # Audio/Generation parameters (from issue 5)
    'chunk_duration_coherent': 8.0,
    'chunk_duration_balanced': 13.0,
    'chunk_duration_speed': 21.0,
    'crossfade_coherent': 1.0,
    'crossfade_balanced': 2.0,
    'crossfade_speed': 3.0,
    'context_coherent': 5.0,
    'context_balanced': 8.0,
    'context_speed': 13.0,
    'temp_bound_min': 0.6,
    'temp_bound_max': 1.4,
    'context_length_limit': 15.0,
    'variation_duration_limit': 20.0,
    'anchor_duration_limit': 10.0,
    'max_chunk_duration': 30.0,
    'overlap_duration': 0.5,
    'tokens_per_second': 50,
    'magic_token_calc': 640,
    
    # UI parameters (from issue 6)
    'max_crossfade_ms': 5000,
    'waveform_point_limit': 5000,
    'note_display_timing_ms': 3000,
}

class ConfigManager:
    """Manages global settings with file persistence and validation."""
    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ConfigManager()
        return cls._instance

    def __init__(self):
        self._settings = DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        """Load settings from file, merging with defaults."""
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    # Merge and validate keys
                    for k, v in file_data.items():
                        if k in self._settings:
                            self._settings[k] = self._validate_value(k, v)
                        else:
                            # Log/Warn unknown setting, but keep it for flexibility
                            self._settings[k] = v
                logger.info(f"Configuration loaded from {SETTINGS_FILE}")
            except Exception as e:
                logger.error(f"Error loading configuration: {e}")
        else:
            logger.info("Settings file not found, using default values.")

    def save(self):
        """Save settings to file."""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2)
            logger.info(f"Configuration saved to {SETTINGS_FILE}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value with validation."""
        self._settings[key] = self._validate_value(key, value)

    def update(self, settings_dict: Dict[str, Any]):
        """Update multiple configuration values."""
        for k, v in settings_dict.items():
            self.set(k, v)
        self.save()

    def get_all(self) -> Dict[str, Any]:
        """Return a copy of all settings."""
        return self._settings.copy()

    def _validate_value(self, key: str, val: Any) -> Any:
        """Perform type and bounds validation on settings."""
        default_val = DEFAULT_SETTINGS.get(key)
        if default_val is None:
            return val  # No default to check against
            
        expected_type = type(default_val)
        
        # Check type
        if expected_type in (int, float) and type(val) in (int, float):
            val = expected_type(val)
        elif not isinstance(val, expected_type):
            logger.warning(f"Type mismatch for config '{key}': expected {expected_type}, got {type(val)}. Using default.")
            return default_val
            
        # Range validation bounds
        if key == 'api_port' and not (1024 <= val <= 65535):
            logger.warning(f"Invalid API port {val}. Using default.")
            return default_val
        if key == 'default_duration' and val < 1:
            return 1
        if key == 'num_workers' and val < 1:
            return 1
        if key == 'pool_size' and val < 1:
            return 1
        if key == 'torch_threads' and val < 1:
            return 1
            
        return val

def get_config(key: str, default: Any = None) -> Any:
    """Helper to get a configuration value."""
    return ConfigManager.instance().get(key, default)

def set_config(key: str, value: Any):
    """Helper to set a configuration value."""
    ConfigManager.instance().set(key, value)

def save_config():
    """Helper to save current config to disk."""
    return ConfigManager.instance().save()
