"""
Kraftbeat Model Cache Manager

Manage HuggingFace model cache - view, analyze, and clear cached models.
Models are stored in the project's 'models' directory.
"""

import logging
import shutil
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from utils.config import get_config

logger = logging.getLogger(__name__)

# Set cache to project directory
_PROJECT_ROOT = Path(__file__).parent.parent.parent  # Go up from utils/ to project root
_MODELS_DIR = Path(get_config("models_dir", str(_PROJECT_ROOT / "models")))

def get_cache_dir() -> Path:
    """Get HuggingFace cache directory (in project models folder)."""
    # Ensure models directory exists
    _MODELS_DIR.mkdir(exist_ok=True)
    
    # Set environment variable so HuggingFace uses our directory
    os.environ["HF_HOME"] = str(_MODELS_DIR)
    os.environ["TRANSFORMERS_CACHE"] = str(_MODELS_DIR / "hub")
    os.environ["HF_HUB_CACHE"] = str(_MODELS_DIR / "hub")
    
    return _MODELS_DIR / "hub"


def get_cached_models() -> List[Dict]:
    """
    Get list of cached models with metadata.
    
    Returns:
        List of dicts with model info: name, size, last_accessed, path
    """
    cache_dir = get_cache_dir()
    if not cache_dir.exists():
        return []
    
    models = []
    
    # HuggingFace stores models in models--org--name format
    for model_dir in cache_dir.glob("models--*"):
        if not model_dir.is_dir():
            continue
        
        try:
            # Parse model name from directory
            parts = model_dir.name.replace("models--", "").split("--")
            if len(parts) >= 2:
                model_name = f"{parts[0]}/{parts[1]}"
            else:
                model_name = parts[0]
            
            # Calculate size
            size = sum(f.stat().st_size for f in model_dir.rglob("*") if f.is_file())
            
            # Get last accessed time
            try:
                mtime = model_dir.stat().st_mtime
                last_accessed = datetime.fromtimestamp(mtime)
            except Exception as e:
                logger.debug(f"Failed to get mtime for {model_dir}: {e}")
                last_accessed = None
            
            models.append({
                'name': model_name,
                'dir_name': model_dir.name,
                'size_bytes': size,
                'size_human': format_size(size),
                'last_accessed': last_accessed,
                'path': str(model_dir),
                'valid': check_model_integrity(str(model_dir))
            })
            
        except Exception as e:
            logger.warning(f"Error reading model {model_dir}: {e}")
    
    # Check for flat models (WinError 1314 workaround)
    flat_dir = _MODELS_DIR / "flat"
    if flat_dir.exists():
        for model_dir in flat_dir.iterdir():
            if not model_dir.is_dir(): continue
            _add_custom_model(model_dir, models, is_flat=True)

    # Check for custom model directories (acestep, diffrhythm, etc.)
    # Scan root models directory for non-hub/non-flat folders
    for model_dir in _MODELS_DIR.iterdir():
        if not model_dir.is_dir(): continue
        if model_dir.name == "hub" or model_dir.name == "flat" or model_dir.name.startswith("models--") or model_dir.name.startswith("."):
            continue
            
        _add_custom_model(model_dir, models, is_flat=False)
            
    # Sort by size (largest first)
    models.sort(key=lambda x: x['size_bytes'], reverse=True)
    return models

def _add_custom_model(model_dir: Path, models: List[Dict], is_flat: bool = False):
    """Helper to process a custom/flat model directory."""
    try:
        raw_name = model_dir.name
        # For flat folders, we might try to infer ID, but for root folders like 'acestep', use exact name
        if is_flat and "_" in raw_name:
             model_id = raw_name.replace("_", "/", 1)
        else:
             model_id = raw_name
        
        # Calculate size
        size = sum(f.stat().st_size for f in model_dir.rglob("*") if f.is_file())
        if size == 0: return # Skip empty folders

        try:
            mtime = model_dir.stat().st_mtime
            last_accessed = datetime.fromtimestamp(mtime)
        except Exception as e:
            logger.debug(f"Failed to get mtime for custom model {model_dir}: {e}")
            last_accessed = None
        
        # Check for duplicates
        if not any(m['name'] == model_id for m in models):
            models.append({
                'name': model_id,
                'dir_name': model_dir.name,
                'size_bytes': size,
                'size_human': format_size(size),
                'last_accessed': last_accessed,
                'path': str(model_dir),
                'is_flat': is_flat,
                'valid': check_model_integrity(str(model_dir))
            })
    except Exception as e:
        logger.warning(f"Error reading custom model {model_dir}: {e}")


def check_model_integrity(model_path: str) -> bool:
    """
    Check if a model directory appears to contain a valid, usable model.
    Verifies existence of config.json and at least one weight file.
    """
    path = Path(model_path)
    if not path.exists():
        return False
        
    # Check for flat structure first (config.json directly in root)
    if (path / "config.json").exists():
        has_config = True
        has_weights = any(f.suffix in ['.bin', '.safetensors', '.pt'] for f in path.iterdir())
        return has_config and has_weights
        
    # Check for HuggingFace Hub structure (snapshots)
    snapshots_dir = path / "snapshots"
    if snapshots_dir.exists():
        # Check all snapshots, if ANY is valid, we're good
        for snapshot in snapshots_dir.iterdir():
            if not snapshot.is_dir(): continue
            
            # Check for broken symlinks or missing files
            try:
                config_file = snapshot / "config.json"
                if config_file.exists(): # This follows symlinks by default
                    # Check for weights
                    has_weights = False
                    for f in snapshot.iterdir():
                        if f.suffix in ['.bin', '.safetensors', '.pt']:
                            if f.exists(): # Verify potentially symlinked file exists
                                has_weights = True
                                break
                    
                    if has_weights:
                        return True
            except Exception as e:
                logger.debug(f"Error checking snapshot in {snapshot}: {e}")
                continue
                
    return False


def format_size(size_bytes: int) -> str:
    """Format bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def get_total_cache_size() -> tuple:
    """
    Get total cache size.
    
    Returns:
        (size_bytes, size_human)
    """
    models = get_cached_models()
    total = sum(m['size_bytes'] for m in models)
    return total, format_size(total)


def delete_model(model_name: str) -> bool:
    """
    Delete a cached model.
    
    Args:
        model_name: Model name like 'facebook/musicgen-small'
        
    Returns:
        True if deleted successfully
    """
    cache_dir = get_cache_dir()
    
    # Convert model name to cache directory name
    dir_name = f"models--{model_name.replace('/', '--')}"
    model_path = cache_dir / dir_name
    
    if not model_path.exists():
        logger.warning(f"Model not found in cache: {model_name}")
        return False
    
    try:
        shutil.rmtree(model_path)
        logger.info(f"Deleted cached model: {model_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete {model_name}: {e}")
        return False


def delete_model_by_path(path: str) -> bool:
    """Delete a cached model by its full path."""
    try:
        shutil.rmtree(path)
        logger.info(f"Deleted: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete {path}: {e}")
        return False


def clear_all_cache() -> bool:
    """
    Clear entire HuggingFace cache.
    
    Returns:
        True if cleared successfully
    """
    cache_dir = get_cache_dir()
    if not cache_dir.exists():
        return True
    
    try:
        shutil.rmtree(cache_dir)
        logger.info("Cleared all cached models")
        return True
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}")
        return False


def get_musicgen_models() -> List[Dict]:
    """Get only MusicGen models from cache."""
    models = get_cached_models()
    return [m for m in models if 'musicgen' in m['name'].lower()]
