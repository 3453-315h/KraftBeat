"""
YuE2 Full-Song Generation Backend for KraftBeat ("AOIDE").

YuE2 is an open-source autoregressive foundation model for full-song music generation
with vocals + accompaniment (48 kHz).
Repo: https://github.com/multimodal-art-projection/YuE
Weights: m-a-p/YuE2-3B & m-a-p/YuE2-Vae
"""

import logging
import os
from pathlib import Path
import time
from typing import Optional, List, Dict, Any
import numpy as np

from src.models.base import MusicGeneratorBase, register_backend
from src.aoide.backend import (
    AoideBackend,
    AoideJob,
    get_aoide_backend,
    YuE2PackageBackend,
)
from src.utils.audio import load_audio

logger = logging.getLogger(__name__)


@register_backend("yue2")
class YuE2Loader(MusicGeneratorBase):
    """
    YuE2 Music Generation Backend ("Aoide").
    
    Generates full songs (vocal + accompaniment) at native 48 kHz stereo.
    Delegates execution to the Aoide backend adapter in an isolated process
    under the global ModelManager GPU lease.
    """

    def __init__(self, route: str = "package"):
        super().__init__()
        self.sample_rate = 48000
        self.route = route
        self._backend: AoideBackend = get_aoide_backend(route)
        self.is_loaded = False

    @property
    def supports_vocals(self) -> bool:
        return True

    @property
    def supports_lyrics(self) -> bool:
        return True

    @property
    def supports_continuation(self) -> bool:
        return False

    @property
    def max_duration(self) -> float:
        # Route 1 has no duration parameter; Route 2 supports up to 900 seconds.
        return 900.0

    @property
    def backend_name(self) -> str:
        return "Aoide (YuE2)"

    def load(self, model_name: str = "yue2-3b", **kwargs) -> bool:
        """Check backend readiness."""
        is_avail, reason = self._backend.is_available()
        if not is_avail:
            logger.warning(f"YuE2 backend unavailable: {reason}")
            self.is_loaded = False
            return False

        self.model_name = model_name
        self.is_loaded = True
        return True

    def generate(
        self,
        prompt: str,
        duration: float = 30.0,
        temperature: float = 1.0,
        lyrics: Optional[str] = None,
        audio_prompt: Optional[np.ndarray] = None,
        melody_audio: Optional[str] = None,
        seed: Optional[int] = None,
        cot: str = "full",
        cfg_scale: float = 1.0,
        **kwargs
    ) -> Optional[np.ndarray]:
        """
        Generate full song audio using YuE2 backend.
        
        Args:
            prompt: Musical style tags
            duration: Target max duration (used only when route == 'comfyui')
            temperature: Creativity / sampling temperature
            lyrics: Song lyrics with [Verse] / [Chorus] tags
            seed: Random seed for reproducibility
            cot: Plan mode ('full' | 'melody' | 'off')
            cfg_scale: Classifier-free guidance scale
            
        Returns:
            np.ndarray of shape [2, samples] (48 kHz stereo) or None on failure
        """
        job_id = f"yue2_{int(time.time())}"
        job = AoideJob(
            job_id=job_id,
            style=prompt,
            lyrics=lyrics or "",
            cot=cot,
            seed=seed,
            cfg_scale=cfg_scale,
            max_duration=duration if self.route == "comfyui" else None,
            route=self.route,
        )

        try:
            self._backend.submit(job)
            
            # Poll for completion
            while True:
                status = self._backend.status(job_id)
                if not status:
                    logger.error("Job status missing.")
                    return None
                if status.state == "done":
                    if status.audio_path and Path(status.audio_path).exists():
                        audio, sr = load_audio(status.audio_path, target_sr=self.sample_rate)
                        return audio
                    logger.error("Job done but audio file not found.")
                    return None
                elif status.state in ("failed", "cancelled"):
                    logger.error(f"Aoide generation {status.state}: {status.error_message}")
                    return None
                time.sleep(0.5)

        except Exception as e:
            logger.error(f"YuE2 generation error: {e}")
            return None

    def unload(self) -> None:
        """Unload backend and release GPU lease."""
        self._backend.unload()
        self.is_loaded = False

    def download_model(self, model_name: str) -> bool:
        """Download model weights from HuggingFace."""
        try:
            from huggingface_hub import snapshot_download
            from src.models.catalog import MODEL_CATALOG

            if model_name in MODEL_CATALOG:
                catalog_key = model_name
            elif model_name in ("yue2", "aoide"):
                catalog_key = "yue2-3b"
            else:
                logger.error(f"Unknown YuE2 model: {model_name}")
                return False

            info = MODEL_CATALOG.get(catalog_key)
            if not info:
                logger.error(f"Unknown YuE2 model: {model_name}")
                return False

            repo_id = info["id"]
            allow_patterns = info.get("allow_patterns", None)

            logger.info(f"Downloading YuE2 weights from {repo_id}...")
            snapshot_download(
                repo_id=repo_id,
                allow_patterns=allow_patterns,
                local_files_only=False,
            )
            logger.info(f"Successfully downloaded YuE2 weights for {model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to download YuE2 weights: {e}")
            return False
