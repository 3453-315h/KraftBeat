"""
ACE-Step Music Generation Backend

ACE-Step is an open-source foundation model for music generation
that produces full-length songs with vocals, comparable to Suno.

GitHub: https://github.com/ace-step/ACE-Step
Features:
- 4 minute songs in ~20 seconds (A100)
- Vocals with lyrics alignment
- Multi-segment structure control
- Voice cloning, style transfer
- Multilingual (19 languages)

Installation:
    pip install git+https://github.com/ace-step/ACE-Step.git
    
VRAM: ~8GB recommended
"""

import logging
import os
from typing import Optional, List, Dict, Any
import numpy as np

from .base import MusicGeneratorBase, register_backend
from .catalog import MODEL_CATALOG
from utils.config import get_config

logger = logging.getLogger(__name__)


# Check if ACE-Step is available
ACE_STEP_AVAILABLE = False
ACEStepPipeline = None
try:
    from acestep.pipeline_ace_step import ACEStepPipeline as _ACEStepPipeline
    ACEStepPipeline = _ACEStepPipeline
    ACE_STEP_AVAILABLE = True
    logger.info("ACE-Step package found")
except ImportError:
    logger.debug("ACE-Step not installed - backend unavailable")


# Default checkpoint cache location
DEFAULT_CHECKPOINT_DIR = get_config(
    "acestep_checkpoint_dir",
    os.path.join(os.getcwd(), "models", "acestep")
)


@register_backend("ace-step")
class ACEStepLoader(MusicGeneratorBase):
    """ACE-Step music generation backend.
    
    Produces full songs with vocals from prompts and lyrics.
    Uses diffusion-based generation with Deep Compression AutoEncoder.
    """
    
    def __init__(self):
        super().__init__()
        self.sample_rate = 44100  # ACE-Step uses 44.1kHz
        self._pipeline: Optional[Any] = None
        self._checkpoint_dir: Optional[str] = None

        
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
        return 240.0  # 4 minutes
    
    @property
    def backend_name(self) -> str:
        return "ACE-Step"
    
    def load(
        self, 
        model_name: str = "default",
        checkpoint_dir: Optional[str] = None,
        device_id: int = 0,
        use_bf16: bool = True,
        cpu_offload: bool = False,
        torch_compile: bool = False,
        **kwargs
    ) -> bool:
        """Load ACE-Step model.
        
        Args:
            model_name: Model variant (currently only "default")
            checkpoint_dir: Path to cached checkpoints (auto-downloads if missing)
            device_id: CUDA device ID
            use_bf16: Use bfloat16 precision (faster, recommended for NVIDIA)
            cpu_offload: Offload weights to CPU to save VRAM
            torch_compile: Use torch.compile for optimization
            
        Returns:
            True if model loaded successfully
        """
        if not ACE_STEP_AVAILABLE:
            logger.error(
                "ACE-Step not installed. Run:\n"
                "  pip install git+https://github.com/ace-step/ACE-Step.git"
            )
            return False
        
        try:
            import torch
            
            # Determine checkpoint directory
            if checkpoint_dir:
                self._checkpoint_dir = checkpoint_dir
            else:
                # Use project-local models folder if it exists
                local_models = os.path.join(os.getcwd(), "models", "ace-step")
                if os.path.exists(local_models):
                    self._checkpoint_dir = local_models
                else:
                    self._checkpoint_dir = DEFAULT_CHECKPOINT_DIR
            
            os.makedirs(self._checkpoint_dir, exist_ok=True)
            
            # Determine dtype
            dtype = "bfloat16" if use_bf16 else "float32"
            
            # Check for MPS (Apple Silicon)
            if torch.backends.mps.is_available():
                dtype = "float32"  # MPS doesn't support bf16 well
                logger.info("Using float32 for Apple Silicon MPS")
            
            logger.info(f"Loading ACE-Step from: {self._checkpoint_dir}")
            logger.info(f"  Device: cuda:{device_id}, dtype: {dtype}")
            logger.info(f"  CPU offload: {cpu_offload}, torch.compile: {torch_compile}")
            
            # Register with ModelManager to unload other models
            from src.utils.model_manager import ModelManager
            ModelManager.instance().prepare_load(self, "ace-step")
            
            # Create pipeline
            self._pipeline = ACEStepPipeline(
                checkpoint_dir=self._checkpoint_dir,
                device_id=device_id,
                dtype=dtype,
                cpu_offload=cpu_offload,
                torch_compile=torch_compile,
            )
            
            # Load checkpoints (downloads from HuggingFace if needed)
            self._pipeline.load_checkpoint(self._checkpoint_dir)
            
            self.model_name = model_name
            self.is_loaded = True
            logger.info("ACE-Step loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load ACE-Step: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    def download_model(self, model_name: str) -> bool:
        """Download model weights from HuggingFace."""
        try:
            from huggingface_hub import snapshot_download
            
            catalog_key = model_name if model_name in MODEL_CATALOG else "acestep"
            repo_id = MODEL_CATALOG[catalog_key]["id"]
            
            target_dir = self._checkpoint_dir
            if not target_dir:
                target_dir = DEFAULT_CHECKPOINT_DIR
                
            logger.info(f"Downloading ACE-Step weights: {repo_id}")
            logger.info(f"Target directory: {target_dir}")
            
            # ensure dir exists
            os.makedirs(target_dir, exist_ok=True)
            
            download_kwargs = {
                "repo_id": repo_id,
                "local_dir": target_dir,
                "resume_download": True
            }
            if "allow_patterns" in MODEL_CATALOG[catalog_key]:
                 download_kwargs["allow_patterns"] = MODEL_CATALOG[catalog_key]["allow_patterns"]
                 logger.info(f"Using allow_patterns: {download_kwargs['allow_patterns']}")
            
            snapshot_download(**download_kwargs)
            
            logger.info("ACE-Step download complete")
            return True
        except Exception as e:
            logger.error(f"ACE-Step download failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate(
        self,
        prompt: str,
        duration: float = 180.0,
        temperature: float = 1.0,
        lyrics: Optional[str] = None,
        audio_prompt: Optional[np.ndarray] = None,
        melody_audio: Optional[str] = None,
        # ACE-Step specific parameters
        guidance_scale: float = 7.0,
        guidance_scale_lyric: float = 2.0,
        infer_steps: int = 60,
        seed: int = -1,
        audio2audio_enable: bool = False,
        ref_audio_strength: float = 0.5,
        **kwargs
    ) -> Optional[np.ndarray]:
        """
        Generate music with ACE-Step.
        
        Args:
            prompt: Style/genre description (tags, mood, instruments)
                   Example: "pop, upbeat, female vocals, synth, 120bpm"
            duration: Target duration (1-240 seconds)
            temperature: Creativity level (not directly used, see guidance_scale)
            lyrics: Song lyrics with optional [verse], [chorus] tags
                   Example: "[verse]\\nHello world\\n[chorus]\\nLa la la"
            guidance_scale: Text prompt guidance (higher = more adherence, 5-15)
            guidance_scale_lyric: Lyrics guidance (1-5)
            infer_steps: Diffusion steps (30-100, more = higher quality)
            seed: Random seed (-1 for random)
            audio2audio_enable: Use audio prompt as reference
            ref_audio_strength: How much to follow audio reference (0-1)
            
        Returns:
            Audio as numpy array [channels, samples] at 44.1kHz
        """
        if not self.is_loaded or self._pipeline is None:
            logger.error("Model not loaded")
            return None
        
        try:
            import torch
            
            # Clamp duration to valid range
            duration = max(1.0, min(duration, self.max_duration))
            
            # Handle seed
            if seed == -1:
                import random
                seed = random.randint(0, 2**31 - 1)
            
            logger.info(f"Generating with ACE-Step:")
            logger.info(f"  Prompt: {prompt[:100]}...")
            logger.info(f"  Duration: {duration}s, Steps: {infer_steps}")
            logger.info(f"  Guidance: {guidance_scale}, Lyric: {guidance_scale_lyric}")
            
            # ref_audio_input should be a file path string, not numpy array
            # ACE-Step pipeline handles loading the audio internally
            ref_audio_path = kwargs.get('ref_audio_path', None)
            if audio2audio_enable and ref_audio_path:
                logger.info(f"  Audio2Audio enabled, reference: {ref_audio_path}")
            
            # Call the pipeline's generation method
            # ACE-Step pipeline typically has a __call__ or generate_music method
            logger.info("Calling ACE-Step pipeline...")
            result = self._pipeline(
                audio_duration=duration,
                prompt=prompt,
                lyrics=lyrics or "",
                infer_step=infer_steps,
                guidance_scale=guidance_scale,
                guidance_scale_lyric=guidance_scale_lyric,
                manual_seeds=[seed],
                audio2audio_enable=audio2audio_enable,
                ref_audio_strength=ref_audio_strength if audio2audio_enable else 0.0,
                ref_audio_input=ref_audio_path if audio2audio_enable else None,
            )
            logger.info(f"Pipeline returned! Type: {type(result)}")
            
            # Aggressive VRAM flushing
            import gc
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                torch.mps.empty_cache()
            
            # Extract audio from result
            # ACE-Step returns different formats depending on version
            if isinstance(result, list):
                # List of audio outputs - take first
                logger.info(f"Result is list of length {len(result)}")
                audio = result[0]
                # If list contains tuples/dicts, extract further
                if isinstance(audio, tuple):
                    audio = audio[0]
                elif isinstance(audio, dict):
                    audio = audio.get('audio', audio.get('waveform', list(audio.values())[0]))
            elif isinstance(result, tuple):
                # (audio, sample_rate) tuple
                logger.info(f"Result is tuple of length {len(result)}")
                audio = result[0]
            elif isinstance(result, dict):
                # Dictionary with 'audio' key
                logger.info(f"Result is dict with keys: {result.keys()}")
                audio = result.get('audio', result.get('waveform', None))
            elif hasattr(result, 'audio'):
                logger.info("Result has .audio attribute")
                audio = result.audio
            else:
                logger.info("Result is raw audio")
                audio = result
            
            logger.info(f"Audio extracted, type: {type(audio)}")
            
            # Handle string (file path) return - ACE-Step sometimes returns path to generated file
            if isinstance(audio, str):
                logger.info(f"Audio is file path: {audio}")
                import soundfile as sf
                audio_data, sr = sf.read(audio)
                logger.info(f"Loaded audio from file: shape={audio_data.shape}, sr={sr}")
                # Transpose if needed (sf.read returns [samples, channels])
                if audio_data.ndim == 2:
                    audio = audio_data.T
                else:
                    audio = audio_data
            
            # Convert to numpy if tensor
            if hasattr(audio, 'cpu'):
                logger.info("Converting tensor to numpy...")
                audio = audio.cpu().numpy()
            
            logger.info(f"Audio shape before reshape: {audio.shape}")
            
            # Ensure shape is [channels, samples]
            if len(audio.shape) == 1:
                # Mono - make stereo
                audio = np.stack([audio, audio], axis=0)
            elif len(audio.shape) == 2 and audio.shape[1] == 2:
                # Shape is [samples, 2], transpose
                audio = audio.T
            elif len(audio.shape) == 3:
                # Batch dimension - take first
                audio = audio[0]
            
            logger.info(f"Generated audio shape: {audio.shape}, sample rate: {self.sample_rate}")
            
            return audio.astype(np.float32)
            
        except Exception as e:
            logger.error(f"ACE-Step generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def unload(self) -> None:
        """Unload model and free memory."""
        if self._pipeline is not None:
            # Call cleanup if available
            if hasattr(self._pipeline, 'cleanup_memory'):
                self._pipeline.cleanup_memory()
            del self._pipeline
            self._pipeline = None
        
        self.is_loaded = False
        
        # Force garbage collection
        import gc
        gc.collect()
        
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError as e:
            logger.debug(f"Torch not imported during ACE-Step unload: {e}")
        
        logger.info("ACE-Step model unloaded")
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return extended capabilities info."""
        base = super().get_capabilities()
        base.update({
            "supports_lyrics_tags": True,  # [verse], [chorus], etc.
            "supports_audio2audio": True,
            "supported_languages": [
                "en", "zh", "ja", "ko", "es", "fr", "de", "pt", "ru",
                "it", "pl", "nl", "tr", "sv", "cs", "ar", "th", "vi"
            ],
            "recommended_guidance": (5.0, 15.0),
            "recommended_steps": (30, 100),
        })
        return base


def is_available() -> bool:
    """Check if ACE-Step can be used."""
    return ACE_STEP_AVAILABLE
