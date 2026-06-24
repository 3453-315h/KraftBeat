"""
DiffRhythm Music Generation Backend

DiffRhythm is an open-source latent diffusion model for music generation
that produces coherent 4m45s songs in approximately 10 seconds.

GitHub: https://github.com/ASLP-lab/DiffRhythm
HuggingFace: https://huggingface.co/spaces/ASLP-lab/DiffRhythm

Features:
- 4 min 45 sec in ~10 seconds generation time
- Latent diffusion architecture (better long-form coherence)
- Synchronized vocals + instrumentals
- Lyrics-to-song generation

Installation:
    git clone https://github.com/ASLP-lab/DiffRhythm.git
    cd DiffRhythm
    pip install -r requirements.txt
    
VRAM: ~12GB recommended
"""

import logging
import sys
import os
from typing import Optional, List, Dict, Any
import numpy as np

from .base import MusicGeneratorBase, register_backend
from .catalog import MODEL_CATALOG
from utils.config import get_config

logger = logging.getLogger(__name__)


# Check if DiffRhythm is available
DIFFRHYTHM_AVAILABLE = False
try:
    # NOTE: Import path may vary - update when testing actual installation
    # DiffRhythm may need to be imported differently
    # Check if DiffRhythm directory exists in common locations
    default_paths = [
        os.path.expanduser("~/DiffRhythm"),
        os.path.join(os.path.dirname(__file__), "..", "..", "DiffRhythm"),
        os.path.join(os.path.dirname(__file__), "..", "..", "models", "diffrhythm", "code"),
    ]
    diffrhythm_paths = get_config("diffrhythm_search_paths", default_paths)
    for path in diffrhythm_paths:
        if os.path.exists(path) and os.path.exists(os.path.join(path, "infer", "infer.py")):
            if path not in sys.path:
                sys.path.insert(0, path)
            DIFFRHYTHM_AVAILABLE = True
            break
            
    if DIFFRHYTHM_AVAILABLE:
        logger.info("DiffRhythm code found")
    else:
        logger.warning(f"DiffRhythm code not found in {diffrhythm_paths}")
        
except Exception as e:
    logger.debug(f"DiffRhythm setup check: {e}")


@register_backend("diffrhythm")
class DiffRhythmLoader(MusicGeneratorBase):
    """DiffRhythm music generation backend."""
    
    def __init__(self):
        super().__init__()
        self.sample_rate = 44100  # DiffRhythm uses 44.1kHz
        self._model = None
    
    @property
    def supports_vocals(self) -> bool:
        return True
    
    @property
    def supports_lyrics(self) -> bool:
        return True  # DiffRhythm requires lyrics
    
    @property
    def supports_continuation(self) -> bool:
        return True  # Can continue existing audio
    
    @property
    def max_duration(self) -> float:
        return 285.0  # 4 minutes 45 seconds
    
    @property
    def backend_name(self) -> str:
        return "DiffRhythm"
    

    def load(self, model_name: str = "default", device_id: int = 0, **kwargs) -> bool:
        """Load DiffRhythm model."""
        if not DIFFRHYTHM_AVAILABLE:
            logger.error("DiffRhythm loading failed: Dependencies/Code missing.")
            return False
        
        try:
            # Setup bundled Espeak if available
            import platform
            system = platform.system()
            if system == "Windows":
                dll_name = "libespeak-ng.dll"
            elif system == "Darwin":
                dll_name = "libespeak-ng.dylib"
            else:
                dll_name = "libespeak-ng.so"
            
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            espeak_dll = os.path.join(root_dir, "models", "bin", "espeak", dll_name)
            
            if os.path.exists(espeak_dll):
                logger.info(f"Checking bundled Espeak: {espeak_dll}")
                os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = espeak_dll
                
                # Apply Runtime Patch to Phonemizer to fix Espeak-NG compatibility
                # This fixes:
                # 1. Access Violation (due to missing data path arg)
                # 2. DLL loading error (due to tempfile copy breaking relative paths)
                try:
                    import phonemizer.backend.espeak.api as espeak_api_module
                    import phonemizer.backend.espeak.wrapper as espeak_wrapper_module
                    import ctypes

                    class PatchedEspeakAPI(espeak_api_module.EspeakAPI):
                        def __init__(self, library):
                            # Skip the tempfile copy logic which breaks espeak-ng data lookup from DLL
                            self._library_path = str(library)
                            # Load in-place
                            if not hasattr(library, 'espeak_Initialize'):
                                self._library = ctypes.cdll.LoadLibrary(self._library_path)
                            else:
                                self._library = library

                            # Determine correct data path (parent of bin)
                            path_arg = None
                            if "PHONEMIZER_ESPEAK_LIBRARY" in os.environ:
                                lib_path = os.environ["PHONEMIZER_ESPEAK_LIBRARY"]
                                bin_dir = os.path.dirname(lib_path)
                                path_arg = bin_dir.encode('utf-8')
                            
                            # Initialize with explicit path
                            # argtypes: output(int), buflength(int), path(char*), options(int)
                            init_func = self._library.espeak_Initialize
                            init_func.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
                            init_func.restype = ctypes.c_int
                            
                            ret = init_func(0x02, 0, path_arg, 0)
                            if ret <= 0:
                                # If already initialized in this process, it might return error, but we proceed
                                # checking real initialization state often requires calling another function.
                                # For now assume if we are here we are trying to init.
                                logger.warning(f"espeak_Initialize returned {ret}, proceeding anyway.")
                                # raise OSError(f"Failed to initialize espeak: {ret}")

                    # Apply Monkeypatch
                    espeak_wrapper_module.EspeakAPI = PatchedEspeakAPI
                    espeak_api_module.EspeakAPI = PatchedEspeakAPI
                    logger.info("Applied EspeakAPI monkeypatch for bundled binary compatibility.")
                    
                except ImportError:
                    logger.warning("Could not patch phonemizer (modules not found)")
                except Exception as e:
                    logger.error(f"Error patching EspeakAPI: {e}")
            else:
                logger.warning(f"Bundled Espeak not found at {espeak_dll}")

            import torch
            import sys
            import contextlib
            
            @contextlib.contextmanager
            def temporary_cwd(path):
                old_pwd = os.getcwd()
                os.chdir(path)
                try:
                    yield
                finally:
                    os.chdir(old_pwd)
            self._cwd_ctx = temporary_cwd
            
            # Setup path to clone dir
            self.code_path = None
            for p in diffrhythm_paths:
                if os.path.exists(p) and os.path.exists(os.path.join(p, "infer", "infer.py")):
                    self.code_path = p
                    break
            
            if not self.code_path:
                 # Try models/diffrhythm/code specifically
                 chk_path = os.path.join(os.getcwd(), "models", "diffrhythm", "code")
                 if os.path.exists(chk_path):
                     self.code_path = chk_path

            if not self.code_path:
                logger.error("DiffRhythm code directory not found")
                return False
                
            # Add 'infer' subdirectory to path
            infer_path = os.path.join(self.code_path, "infer")
            if infer_path not in sys.path:
                sys.path.insert(0, infer_path) 
            
            # Import functions
            try:
                from infer import inference as dr_inference
                from infer_utils import prepare_model, get_lrc_token, get_style_prompt, get_negative_style_prompt, get_reference_latent
                
                self._dr_inference = dr_inference
                self._dr_prepare = prepare_model
                self._dr_lrc = get_lrc_token
                self._dr_style = get_style_prompt
                self._dr_neg = get_negative_style_prompt
                self._dr_ref = get_reference_latent
                
            except ImportError as e:
                logger.error(f"Failed to import DiffRhythm functions: {e}")
                return False

            # Initialize Model - detect best device
            if torch.cuda.is_available():
                device = f"cuda:{device_id}"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                device = "mps"
            else:
                device = "cpu"
            self.max_frames = get_config("diffrhythm_max_frames", 6144)  # Support up to 285s (was 2048 for 95s only)
            
            # Register with ModelManager to unload other models
            from src.utils.model_manager import ModelManager
            ModelManager.instance().prepare_load(self, "diffrhythm")
            
            logger.info(f"Loading DiffRhythm models on {device}...")
            # Wrap preparation in CWD context to find ./config and ./g2p
            with self._cwd_ctx(self.code_path):
                self._models = self._dr_prepare(self.max_frames, device)
                
            self._device = device
            
            self.model_name = model_name
            self.is_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to load DiffRhythm: {e}")
            import traceback
            traceback.print_exc()
            return False

    def download_model(self, model_name: str) -> bool:
        """Download model weights from HuggingFace."""
        try:
            from huggingface_hub import snapshot_download
            
            catalog_key = model_name if model_name in MODEL_CATALOG else "diffrhythm"
            repo_id = MODEL_CATALOG[catalog_key]["id"]
            
            # Save to project local models/diffrhythm
            target_dir = os.path.join(os.getcwd(), "models", "diffrhythm")
                
            logger.info(f"Downloading DiffRhythm weights: {repo_id}")
            logger.info(f"Target directory: {target_dir}")
            
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
            
            logger.info("DiffRhythm download complete")
            return True
        except Exception as e:
            logger.error(f"DiffRhythm download failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generate(
        self,
        prompt: str,
        duration: float = 285.0, # Default to full length
        temperature: float = 1.0,
        lyrics: Optional[str] = None,
        audio_prompt: Optional[np.ndarray] = None,
        melody_audio: Optional[str] = None,
        **kwargs
    ) -> Optional[np.ndarray]:
        """
        Generate music with DiffRhythm.
        """
        if not self.is_loaded:
            logger.error("Model not loaded")
            return None
        
        if not lyrics:
             lyrics = f"[00:00.00]{prompt}" 
        
        try:
            logger.info(f"Generating DiffRhythm: '{prompt}' ({duration}s)")
            
            # Map components
            cfm, tokenizer, muq, vae = self._models
            
            # Switch CWD for generation (needed for negative prompt file)
            with self._cwd_ctx(self.code_path):
                # Prepare inputs
                target_len = int(duration)
                min_len = get_config("diffrhythm_min_len", 95)
                max_len = get_config("diffrhythm_max_len", 285)
                if target_len <= min_len:
                    target_len = min_len
                elif target_len > max_len:
                    target_len = max_len
                    
                lrc_prompt, start_time, end_frame, song_duration = self._dr_lrc(self.max_frames, lyrics, tokenizer, target_len, self._device)
                
                # Style Prompt
                style_prompt = self._dr_style(muq, prompt=prompt)
                
                # Negative Prompt (loads local file)
                neg_prompt = self._dr_neg(self._device)
                
                # Latents
                latent_prompt, pred_frames = self._dr_ref(self._device, self.max_frames, False, None, None, vae)
                
                # Call inference
                steps = kwargs.get('steps', 32)
                cfg_strength = kwargs.get('cfg_strength', 4.0)
                
                generated_songs = self._dr_inference(
                    cfm_model=cfm,
                    vae_model=vae,
                    cond=latent_prompt,
                    text=lrc_prompt,
                    duration=end_frame,
                    style_prompt=style_prompt,
                    negative_style_prompt=neg_prompt,
                    start_time=start_time,
                    pred_frames=pred_frames,
                    batch_infer_num=1,
                    song_duration=song_duration,
                    steps=steps,
                    cfg_strength=cfg_strength
                )
                
                audio_result = generated_songs[0] # List of tensors
                
                # Aggressive VRAM flushing
                import gc
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                    torch.mps.empty_cache()
                
                
            # Convert result to numpy [channels, samples]
            if hasattr(audio_result, 'cpu'):
                audio = audio_result.cpu().numpy()
            else:
                audio = audio_result
                
            return audio.astype(np.float32)
            
        except Exception as e:
            logger.error(f"DiffRhythm generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None

    def unload(self) -> None:
        """Unload model and free memory."""
        if hasattr(self, '_models') and self._models is not None:
            del self._models
            self._models = None
        
        if self._model is not None:
            del self._model
            self._model = None
            
        self.is_loaded = False
        
        # Force garbage collection
        import gc
        gc.collect()
        
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError as e:
            logger.debug(f"Torch not imported during DiffRhythm unload: {e}")
        
        logger.info("DiffRhythm model unloaded")


def is_available() -> bool:
    """Check if DiffRhythm can be used."""
    return DIFFRHYTHM_AVAILABLE
