"""
Model Manager for Kraftbeat.

Ensures that only one heavy AI model is loaded in VRAM at a time.
"""

import logging
import gc
from typing import Optional, Any

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Singleton manager to enforce 'Single Active Model' policy.
    
    Usage:
        ModelManager.instance().prepare_load(new_loader)
    """
    
    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ModelManager()
        return cls._instance
        
    def __init__(self):
        self.active_loader: Optional[Any] = None
        self.active_model_name: str = ""
        
    def prepare_load(self, loader: Any, model_name: str = "") -> None:
        """
        Call this BEFORE loading a new model.
        It checks if a different loader is active and unloads it.
        """
        if self.active_loader is not None and self.active_loader != loader:
            logger.info(f"Unloading previous model from {self.active_loader.__class__.__name__}...")
            try:
                if hasattr(self.active_loader, 'unload'):
                    self.active_loader.unload()
                else:
                    logger.warning(f"Active loader {self.active_loader} has no unload() method!")
            except Exception as e:
                logger.error(f"Error unloading previous model: {e}")
                
            self.active_loader = None
            self.force_cleanup()
            
        # Register the new loader as active (even if loading fails later, we track it)
        self.active_loader = loader
        self.active_model_name = model_name
        
    def force_cleanup(self):
        """Force Python GC and CUDA cache cleanup."""
        gc.collect()
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
        except ImportError as e:
            logger.debug(f"Torch not imported during cleanup: {e}")
        logger.info("VRAM cleanup performed.")

    def get_active_model_name(self) -> str:
        return self.active_model_name

