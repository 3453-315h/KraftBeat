"""
Base interface for all music generation backends.
This provides a unified API so the UI can work with any backend.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import numpy as np


class MusicGeneratorBase(ABC):
    """Abstract base class for music generation backends."""
    
    def __init__(self):
        self.model = None
        self.model_name: str = ""
        self.sample_rate: int = 32000
        self.is_loaded: bool = False
    
    @abstractmethod
    def load(self, model_name: str, **kwargs) -> bool:
        """Load the model. Returns True if successful."""
        pass
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        duration: float = 30.0,
        temperature: float = 1.0,
        lyrics: Optional[str] = None,
        audio_prompt: Optional[np.ndarray] = None,
        melody_audio: Optional[str] = None,
        **kwargs
    ) -> Optional[np.ndarray]:
        """
        Generate audio from prompt.
        
        Args:
            prompt: Text description of desired music
            duration: Target duration in seconds
            temperature: Creativity (0.5 = stable, 1.5 = creative)
            lyrics: Optional lyrics for vocal models
            audio_prompt: Optional audio context for continuation
            melody_audio: Optional melody file path for conditioning
            
        Returns:
            numpy array of shape [channels, samples] or None on failure
        """
        pass
    
    @abstractmethod
    def unload(self) -> None:
        """Unload model and free memory."""
        pass
    
    @property
    @abstractmethod
    def supports_vocals(self) -> bool:
        """Whether this backend can generate vocals."""
        pass
    
    @property
    @abstractmethod
    def supports_lyrics(self) -> bool:
        """Whether this backend accepts lyrics input."""
        pass
    
    @property
    @abstractmethod
    def supports_continuation(self) -> bool:
        """Whether this backend can continue from audio context."""
        pass
    
    @property
    @abstractmethod
    def max_duration(self) -> float:
        """Maximum single-generation duration in seconds."""
        pass
    
    @property
    def backend_name(self) -> str:
        """Human-readable backend name."""
        return self.__class__.__name__
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return backend capabilities for UI display."""
        return {
            "name": self.backend_name,
            "vocals": self.supports_vocals,
            "lyrics": self.supports_lyrics,
            "continuation": self.supports_continuation,
            "max_duration": self.max_duration,
            "sample_rate": self.sample_rate,
        }


# Registry of available backends
BACKENDS: Dict[str, type] = {}


def register_backend(name: str):
    """Decorator to register a backend class."""
    def decorator(cls):
        BACKENDS[name] = cls
        return cls
    return decorator


def get_backend(name: str) -> Optional[MusicGeneratorBase]:
    """Get an instance of a backend by name."""
    if name in BACKENDS:
        return BACKENDS[name]()
    return None


def list_backends() -> List[str]:
    """List available backend names."""
    return list(BACKENDS.keys())
