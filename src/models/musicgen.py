"""
Kraftbeat MusicGen Model Loader

Handles loading and inference for MusicGen models.
Uses audiocraft (Meta's library) first, falls back to Hugging Face Transformers.
"""

import logging
import os
import numpy as np
from typing import Optional, List
from enum import Enum

# ============================================================================
# COMPATIBILITY PATCH: Fix audiocraft on DirectML/non-CUDA systems
# audiocraft/xformers checks torch.backends.cuda.is_flash_attention_available()
# which doesn't exist on non-CUDA PyTorch builds. We patch it here.
# ============================================================================
try:
    import torch
    if not hasattr(torch.backends.cuda, 'is_flash_attention_available'):
        # Monkey-patch the missing function
        torch.backends.cuda.is_flash_attention_available = lambda: False
        logging.getLogger(__name__).info("Patched torch.backends.cuda.is_flash_attention_available for DirectML compatibility")
except Exception as e:
    logging.getLogger(__name__).warning(f"Could not apply CUDA compatibility patch: {e}")
# ============================================================================

# ============================================================================
# COMPATIBILITY PATCH: Fix torch-directml unknown error in torch.embedding
# and reflection/replication padding operator compatibility issues on DirectML.
# ============================================================================
try:
    import torch.nn as nn
    import torch.nn.functional as F

    # nn.Embedding patch removed because native embedding lookup works on DirectML with long tensors

    # 2. Padding Patch (Global C++ level patch to avoid DirectML reflect/replicate crashes)
    original_c_pad = torch._C._nn.pad

    def patched_c_pad(input, pad, mode="constant", value=None):
        if mode in ('reflect', 'replicate') and input.device.type in ('privateuseone', 'dml'):
            # CPU fallback: cast to float32 on CPU (since CPU PyTorch lacks float16 pad support)
            cpu_input = input.to('cpu').float()
            cpu_output = original_c_pad(cpu_input, pad, mode, value)
            return cpu_output.to(input.device).to(dtype=input.dtype)
        else:
            return original_c_pad(input, pad, mode, value)

    torch._C._nn.pad = patched_c_pad

    # 3. build_delay_pattern_mask Boolean Type Promotion Patch
    # On DirectML, multiplying a torch.bool mask by a torch.long tensor coerces the
    # result to torch.bool (token IDs become 0/1), corrupting the pattern and triggering
    # C++ assertion failures (dml_util.h:52) during the generation loop.
    # Fix: cast bool masks to long before the multiplication so the result stays int64.
    try:
        from transformers.models.musicgen.modeling_musicgen import MusicgenForCausalLM

        _original_build_delay_pattern_mask = MusicgenForCausalLM.build_delay_pattern_mask

        def _patched_build_delay_pattern_mask(self, input_ids, pad_token_id, max_length=None):
            input_ids = input_ids.reshape(-1, self.num_codebooks, input_ids.shape[-1])
            bsz, num_codebooks, seq_len = input_ids.shape
            max_length = max_length if max_length is not None else self.generation_config.max_length
            import torch as _torch
            input_ids_shifted = (
                _torch.ones((bsz, num_codebooks, max_length), dtype=_torch.long, device=input_ids.device) * -1
            )
            channel_codebooks = num_codebooks // 2 if self.config.audio_channels == 2 else num_codebooks
            if max_length < 2 * channel_codebooks - 1:
                return input_ids.reshape(bsz * num_codebooks, -1), input_ids_shifted.reshape(bsz * num_codebooks, -1)
            for codebook in range(channel_codebooks):
                if self.config.audio_channels == 1:
                    input_ids_shifted[:, codebook, codebook: seq_len + codebook] = input_ids[:, codebook]
                else:
                    input_ids_shifted[:, 2 * codebook, codebook: seq_len + codebook] = input_ids[:, 2 * codebook]
                    input_ids_shifted[:, 2 * codebook + 1, codebook: seq_len + codebook] = input_ids[:, 2 * codebook + 1]
            delay_pattern = _torch.triu(
                _torch.ones((channel_codebooks, max_length), dtype=_torch.bool),
                diagonal=max_length - channel_codebooks + 1,
            )
            delay_pattern = delay_pattern + _torch.tril(_torch.ones((channel_codebooks, max_length), dtype=_torch.bool))
            if self.config.audio_channels == 2:
                delay_pattern = delay_pattern.repeat_interleave(2, dim=0)
            mask = ~delay_pattern.to(input_ids.device)
            # NOTE: Cast masks to long (int64) to prevent DirectML boolean type promotion
            # bug where bool * int64 returns bool instead of int64, corrupting token IDs.
            mask_long = mask.long()
            neg_mask_long = (~mask).long()
            if isinstance(pad_token_id, _torch.Tensor):
                pad_val = pad_token_id.long()
            else:
                pad_val = int(pad_token_id)
            input_ids = mask_long * input_ids_shifted + neg_mask_long * pad_val
            first_codebook_ids = input_ids[:, 0, :]
            start_ids = (first_codebook_ids == -1).nonzero()[:, 1]
            if len(start_ids) > 0:
                first_start_id = min(start_ids)
            else:
                first_start_id = seq_len
            pattern_mask = input_ids.reshape(bsz * num_codebooks, -1)
            input_ids = input_ids[..., :first_start_id].reshape(bsz * num_codebooks, -1)
            return input_ids, pattern_mask

        MusicgenForCausalLM.build_delay_pattern_mask = _patched_build_delay_pattern_mask
        logging.getLogger(__name__).info("Patched MusicgenForCausalLM.build_delay_pattern_mask for DirectML boolean type promotion bug")

        # 4. apply_delay_pattern_mask Patch
        # torch.where(decoder_pad_token_mask == -1, ...) creates a bool tensor from the
        # == -1 comparison; on DirectML this bools-as-mask path triggers dml_util.h:52.
        # Fix: Use explicit integer arithmetic instead of torch.where with bool condition.
        import torch as _torch_patch

        @staticmethod
        def _patched_apply_delay_pattern_mask(input_ids, decoder_pad_token_mask):
            seq_len = input_ids.shape[-1]
            mask = decoder_pad_token_mask[..., :seq_len]
            # Where mask == -1, keep input_ids; elsewhere use the mask value.
            # Rewrite as: out = input_ids * (mask == -1) + mask * (mask != -1)
            # Use long() to ensure no boolean dtype on DirectML.
            use_input = (mask == -1).long()  # 1 where we want input_ids, 0 elsewhere
            use_mask  = (mask != -1).long()  # 1 where we want mask value, 0 elsewhere
            return input_ids * use_input + mask * use_mask

        MusicgenForCausalLM.apply_delay_pattern_mask = _patched_apply_delay_pattern_mask
        logging.getLogger(__name__).info("Patched MusicgenForCausalLM.apply_delay_pattern_mask for DirectML torch.where boolean bug")

        # Unused post-processing patch removed (native boolean indexing works fine on DirectML)
        pass

    except Exception as _patch_err:
        logging.getLogger(__name__).warning(f"Could not patch build_delay_pattern_mask: {_patch_err}")

    logging.getLogger(__name__).info("Patched nn.Embedding, torch._C._nn.pad, delay pattern masks for DirectML compatibility")
except Exception as e:
    logging.getLogger(__name__).warning(f"Could not apply DirectML compatibility patches: {e}")
# ============================================================================

logger = logging.getLogger(__name__)


class LoaderBackend(Enum):
    """Which backend is being used."""
    AUDIOCRAFT = "audiocraft"
    TRANSFORMERS = "transformers"
    NONE = "none"


# Available MusicGen models with their properties
from .catalog import MODEL_CATALOG as MUSICGEN_MODELS
from .base import MusicGeneratorBase
from src.utils.model_manager import ModelManager
from utils.config import get_config


class MusicGenLoader(MusicGeneratorBase):
    """
    Handles MusicGen model loading and generation.
    
    Priority:
    1. audiocraft (Meta's official library) - more features
    2. Hugging Face Transformers - fallback for compatibility
    """
    
    
    def __init__(self, device_info):
        """
        Initialize the model loader.
        
        Args:
            device_info: DeviceInfo object from device.py
        """
        self.device_info = device_info
        
        # Ensure proper defaults for device info if None passed (e.g., during download)
        if self.device_info is None:
            try:
                from src.device import DeviceInfo, DeviceType
            except ImportError:
                try:
                    from device import DeviceInfo, DeviceType
                except ImportError:
                    logger.error("Could not import device module")
                    raise
            self.device_info = DeviceInfo(DeviceType.CPU, "CPU", "cpu")
        
        super().__init__()
        self.processor = None
        self._sample_rate = 32000
        self.backend = LoaderBackend.NONE
        
    @property
    def supports_vocals(self) -> bool:
        return False
    
    @property
    def supports_lyrics(self) -> bool:
        return False

    @property
    def supports_continuation(self) -> bool:
        return True 

    @property
    def max_duration(self) -> float:
        return 30.0
             
    @property
    def sample_rate(self) -> int:
        """Return the model's sample rate."""
        return self._sample_rate
        
    @sample_rate.setter
    def sample_rate(self, value: int):
        self._sample_rate = value
        
    def get_available_models(self) -> List[str]:
        """Return list of model names."""
        return list(MUSICGEN_MODELS.keys())
    
    def load(self, model_name: str, **kwargs) -> bool:
        """Alias for load_model to satisfy abstract base class."""
        precision = kwargs.get('precision', 'fp32')
        return self.load_model(model_name, precision=precision)

    def load_model(self, model_name: str = "small", precision: str = "fp32") -> bool:
        """
        Load a MusicGen model. Tries audiocraft first, then Transformers.
        
        Args:
            model_name: One of the MUSICGEN_MODELS keys
            precision: 'fp32', 'fp16', 'int8', 'int4'
            
        Returns:
            True if successful, False otherwise
        """
        if model_name not in MUSICGEN_MODELS:
            logger.error(f"Unknown model: {model_name}")
            return False
            
        model_info = MUSICGEN_MODELS[model_name]
        model_id = model_info["id"]
        
        logger.info(f"Loading MusicGen model: {model_id}")
        logger.info(f"  Parameters: {model_info['params']}")
        logger.info(f"  VRAM Required: ~{model_info['vram_gb']} GB")
        
        # Register with ModelManager to unload other models
        ModelManager.instance().prepare_load(self, model_name)

        # Check if we are using DirectML
        is_directml = False
        from src.device import DeviceType
        if self.device_info and self.device_info.device_type == DeviceType.DIRECTML:
            is_directml = True
        if hasattr(self, 'device_info') and hasattr(self.device_info, 'device_obj') and hasattr(self.device_info.device_obj, 'type'):
             if self.device_info.device_obj.type == 'privateuseone':
                 is_directml = True

        if is_directml and precision in ('fp16', 'int8', 'int4'):
            logger.warning(f"DirectML backend does not support stable execution of '{precision}' precision for this model.")
            logger.warning("Falling back to float32 ('fp32') to prevent fatal C++ driver crash [dml_util.h:52].")
            precision = "fp32"
            
        # Quantization forces Transformers backend
        if precision in ['int8', 'int4']:
            is_directml = False
            from src.device import DeviceType
            if self.device_info and self.device_info.device_type == DeviceType.DIRECTML:
                is_directml = True
            if hasattr(self, 'device_info') and hasattr(self.device_info, 'device_obj') and hasattr(self.device_info.device_obj, 'type'):
                 if self.device_info.device_obj.type == 'privateuseone':
                     is_directml = True
            
            if is_directml:
                logger.warning(f"Quantization ({precision}) is not supported on DirectML. Falling back to float16...")
                precision = "fp16"
            else:
                logger.info(f"Quantization ({precision}) requested, forcing Transformers backend...")
                if self._try_load_transformers(model_id, model_name, precision):
                    return True
                return False
        
        # DirectML Optimization: Audiocraft DOES NOT support DirectML.
        # If we are on AMD/Intel, we MUST use Transformers to get GPU acceleration.
        # Otherwise Audiocraft will force CPU.
        is_directml = False
        from src.device import DeviceType
        if self.device_info and self.device_info.device_type == DeviceType.DIRECTML:
            is_directml = True
            
        # Also check device object itself just in case
        if hasattr(self.device_info, 'device_obj') and hasattr(self.device_info.device_obj, 'type'):
             if self.device_info.device_obj.type == 'privateuseone':
                 is_directml = True

        if is_directml and "magnet" not in model_id.lower():
            logger.info("DirectML detected: Prioritizing Transformers backend for GPU acceleration.")
            if self._try_load_transformers(model_id, model_name, precision):
                return True
            logger.warning("Transformers load failed on DirectML, trying audiocraft (will be CPU only)...")
        
        # Try audiocraft first (more features, but CPU-only on DirectML)
        if self._try_load_audiocraft(model_id, model_name):
            # If we loaded audiocraft on a GPU system that isn't Nvidia, warn user
            if is_directml:
                 logger.warning("NOTE: Model loaded with audiocraft on CPU. For GPU speed, Transformers backend is preferred but failed to load.")
            return True
        
        # Fall back to Transformers
        logger.info("Falling back to Transformers API...")
        if self._try_load_transformers(model_id, model_name, precision):
            return True
        
        logger.error("Failed to load model with both audiocraft and Transformers")
        return False
    
    def _get_flat_storage_path(self, model_id: str):
        """Get path for flat model storage (no symlinks)."""
        from pathlib import Path
        root = Path(__file__).parent.parent.parent
        sanitized = model_id.replace("/", "_")
        return root / "models" / "flat" / sanitized

    def _resolve_model_path(self, model_id: str) -> str:
        """Resolve model ID to local path if it exists in flat storage."""
        flat_path = self._get_flat_storage_path(model_id)
        if flat_path.exists():
            logger.info(f"Found local flat model: {flat_path}")
            return str(flat_path)
        return model_id

    def download_model(self, model_name: str) -> bool:
        """
        Explicitly download a model to cache without loading it.
        This allows for a 'Download' button in the UI.
        """
        if model_name not in MUSICGEN_MODELS:
            return False
            
        model_id = MUSICGEN_MODELS[model_name]["id"]
        logger.info(f"Downloading model {model_id}...")
        
        try:
            from huggingface_hub import snapshot_download
            
            try:
            # Try standard HF cache first (uses symlinks)
                download_kwargs = {"repo_id": model_id}
                if "allow_patterns" in MUSICGEN_MODELS[model_name]:
                     download_kwargs["allow_patterns"] = MUSICGEN_MODELS[model_name]["allow_patterns"]
                     logger.info(f"Using allow_patterns: {download_kwargs['allow_patterns']}")
                
                snapshot_download(**download_kwargs)
                logger.info(f"Model {model_id} downloaded successfully (standard cache).")
                return True
            except (OSError, PermissionError) as e:
                # Catch Windows symlink error (WinError 1314)
                if "1314" in str(e) or "privilege" in str(e).lower() or "symlink" in str(e).lower():
                    logger.warning(f"Standard download failed due to permissions (symlinks). Falling back to flat usage: {e}")
                    
                    target_path = self._get_flat_storage_path(model_id)
                    logger.info(f"Downloading to flat directory: {target_path}")
                    
                    if "allow_patterns" in MUSICGEN_MODELS[model_name]:
                        download_kwargs["allow_patterns"] = MUSICGEN_MODELS[model_name]["allow_patterns"]

                    snap_kwargs = {
                        "repo_id": model_id,
                        "local_dir": target_path,
                        "local_dir_use_symlinks": False,
                    }
                    if "allow_patterns" in MUSICGEN_MODELS[model_name]:
                        snap_kwargs["allow_patterns"] = MUSICGEN_MODELS[model_name]["allow_patterns"]
                        
                    snapshot_download(**snap_kwargs)
                    logger.info(f"Model {model_id} downloaded successfully (flat mode).")
                    return True
                raise e
                
        except Exception as e:
            logger.error(f"Failed to download model {model_id}: {e}")
            return False
    
    def _try_load_audiocraft(self, model_id: str, model_name: str) -> bool:
        """Try loading with audiocraft library."""
        try:
            import xformers
            from audiocraft.models import MusicGen, AudioGen, MAGNeT
            
            logger.info("Using audiocraft backend...")
            
            # Resolve path (check flat storage)
            load_path = self._resolve_model_path(model_id)
            
            # Load model
            # We try to use the device if available.
            # Note: audiocraft internally often hardcodes 'cuda' checks, but our monkey patch might help.
            device_to_use = 'cpu'
            if self.device_info and self.device_info.device_obj:
                device_to_use = self.device_info.device_obj
                logger.info(f"Attempting to load audiocraft model on: {device_to_use}")
            else:
                logger.info("Loading model on CPU...")
            
            if "audiogen" in model_id.lower():
                 logger.info(f"Detected AudioGen model: {model_id}")
                 self.model = AudioGen.get_pretrained(load_path, device=device_to_use)
            elif "magnet" in model_id.lower():
                 logger.info(f"Detected MAGNeT model: {model_id}")
                 self.model = MAGNeT.get_pretrained(load_path, device=device_to_use)
            else:
                 self.model = MusicGen.get_pretrained(load_path, device=device_to_use)
            
            self.model_name = model_name
            self._sample_rate = self.model.sample_rate
            self.backend = LoaderBackend.AUDIOCRAFT
            
            logger.info(f"Model loaded with audiocraft on {device_to_use}")
            return True
            
        except ImportError as e:
            logger.info(f"audiocraft not found ({e}), falling back to transformers (Standard for DirectML)")
            return False
        except Exception as e:
            logger.warning(f"audiocraft load failed: {e}, will try Transformers")
            return False
    
    def _try_load_transformers(self, model_id: str, model_name: str, precision: str = "fp32") -> bool:
        """Try loading with Hugging Face Transformers."""
        try:
            import torch
            from transformers import AutoProcessor, MusicgenForConditionalGeneration
            
            logger.info("Using Transformers backend...")
            
            # Resolve path (check flat storage)
            load_path = self._resolve_model_path(model_id)
            
            # Check environment settings
            # NOTE: Flash Attention 2 ONLY works on CUDA with specific NVIDIA GPUs
            # It does NOT work on DirectML/AMD - always disable it
            use_flash_attn = False  # Disabled for DirectML compatibility
            use_better_transformer = os.environ.get('KRAFTBEAT_BETTER_TRANSFORMER', '0') == '1'
            
            # Quantization config
            quant_config = None
            dtype = torch.float32
            
            if precision == 'int4':
                try:
                    import bitsandbytes
                    from transformers import BitsAndBytesConfig
                    quant_config = BitsAndBytesConfig(
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=torch.float16,
                    )
                    logger.info("Using 4-bit quantization config")
                except ImportError:
                    logger.warning("bitsandbytes not installed, ignoring 4-bit request")
            elif precision == 'int8':
                try:
                    import bitsandbytes
                    from transformers import BitsAndBytesConfig
                    quant_config = BitsAndBytesConfig(load_in_8bit=True)
                    logger.info("Using 8-bit quantization config")
                except ImportError:
                    logger.warning("bitsandbytes not installed, ignoring 8-bit request")
            elif precision == 'fp16':
                dtype = torch.float16
                logger.info("Using float16 precision")
            
            # Load processor
            self.processor = AutoProcessor.from_pretrained(load_path)
            
            # Load model class based on type
            if "audiogen" in model_id.lower():
                try:
                    from transformers import AudiogenForConditionalGeneration
                    ModelClass = AudiogenForConditionalGeneration
                except ImportError:
                    logger.error("AudiogenForConditionalGeneration not available in installed transformers version.")
                    return False
            elif "magnet" in model_id.lower():
                # MAGNeT is NOT supported in transformers library!
                # It only works with audiocraft.
                logger.error("MAGNeT models are NOT supported via Transformers. They ONLY work with audiocraft library.")
                logger.error("Install audiocraft to use MAGNeT models: pip install audiocraft")
                return False
            else:
                ModelClass = MusicgenForConditionalGeneration

            # Load model
            logger.info(f"Loading model with {ModelClass.__name__}...")
            
            load_kwargs = {}
            if quant_config:
                load_kwargs['quantization_config'] = quant_config
                load_kwargs['device_map'] = "auto"
            else:
                load_kwargs['torch_dtype'] = dtype
            
            # DirectML compatibility: force eager attention to avoid SDPA C++ crashes
            load_kwargs['attn_implementation'] = "eager"
            logger.info("Forcing eager attention implementation for DirectML compatibility.")
            
            self.model = ModelClass.from_pretrained(load_path, **load_kwargs)
            
            # Move to device if available and not using device_map
            if self.device_info and self.model.device.type == 'cpu':
                logger.info(f"Moving model to {self.device_info.device_obj}...")
                try:
                    self.model = self.model.to(self.device_info.device_obj)
                except Exception as e:
                    logger.warning(f"Failed to move model to device, falling back to CPU: {e}")
            
            # Detect DirectML device inside _try_load_transformers for conditional patches
            _is_directml = False
            try:
                from src.device import DeviceType as _DeviceType
                if self.device_info and self.device_info.device_type == _DeviceType.DIRECTML:
                    _is_directml = True
            except ImportError:
                pass
            if hasattr(self.device_info, 'device_obj') and hasattr(self.device_info.device_obj, 'type'):
                if self.device_info.device_obj.type == 'privateuseone':
                    _is_directml = True
            
            # DirectML Encodec CPU Fallback Patch:
            # EncodecModel uses a fused LSTM kernel (aten::_thnn_fused_lstm_cell) that
            # DirectML's CPU fallback bridge cannot dispatch. We keep the audio encoder
            # on the CPU so its decode() call succeeds, but we transparently move
            # input codes to CPU before decode and move audio_values back to the GPU
            # after, so the rest of the pipeline works on the GPU as expected.
            if _is_directml and hasattr(self.model, 'audio_encoder'):
                logger.info("Keeping EncodecModel audio_encoder on CPU for DirectML LSTM compatibility.")
                try:
                    self.model.audio_encoder = self.model.audio_encoder.to('cpu')
                    _original_audio_enc_decode = self.model.audio_encoder.decode
                    _dml_device = self.device_info.device_obj

                    def _dml_audio_encoder_decode(codes, audio_scales=None, **kw):
                        if isinstance(codes, torch.Tensor):
                            codes = codes.to('cpu')
                        result = _original_audio_enc_decode(codes, audio_scales=audio_scales, **kw)
                        if hasattr(result, 'audio_values') and isinstance(result.audio_values, torch.Tensor):
                            result.audio_values = result.audio_values.to(_dml_device)
                        return result

                    self.model.audio_encoder.decode = _dml_audio_encoder_decode
                    logger.info("Wrapped audio_encoder.decode with DirectML CPU bridge successfully.")
                except Exception as enc_e:
                    logger.warning(f"Could not apply audio_encoder CPU bridge: {enc_e}")

            self.model_name = model_name
            self._sample_rate = self.model.config.audio_encoder.sampling_rate
            self.backend = LoaderBackend.TRANSFORMERS
            
            logger.info(f"Model loaded with Transformers ({precision})")
            return True
            
        except ImportError as e:
            missing_module = getattr(e, 'name', None)
            if missing_module in ['transformers', 'torch'] or (missing_module is None and 'transformers' in str(e).lower()):
                logger.error(f"transformers not installed: {e}")
            else:
                logger.error(f"{e}")
            return False
        except Exception as e:
            logger.error(f"Transformers failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate(
        self,
        prompt: str,
        duration: float = 8.0,
        temperature: float = 1.0,
        top_k: int = 250,
        top_p: float = 0.0,
        cfg_coef: float = 3.0,
        melody_audio: Optional[str] = None,
        audio_prompt: Optional[object] = None, # Numpy array for continuation
        progress_callback=None,
    ):
        """
        Generate audio from text prompt.
        
        Args:
            prompt: Text description of desired music
            duration: Length in seconds (max 30)
            temperature: Creativity (0.0-2.0, default 1.0)
            top_k: Token diversity (1-250, default 250)
            top_p: Nucleus sampling (0.0-1.0, 0 = disabled)
            cfg_coef: Prompt adherence (1.0-10.0, default 3.0)
            melody_audio: Path to audio file for melody conditioning
            audio_prompt: Optional numpy array (channels, samples) for continuation
            progress_callback: Optional callback(current, total)
            
        Returns:
            Generated audio as numpy array, or None on failure
        """
        if self.model is None:
            raise RuntimeError("No model loaded. Please select a model and wait for it to load.")
        
        if self.backend == LoaderBackend.AUDIOCRAFT:
            return self._generate_audiocraft(
                prompt, duration, temperature, top_k, top_p, cfg_coef,
                melody_audio, progress_callback
            )
        else:
            return self._generate_transformers(
                prompt, duration, temperature, top_k, top_p, cfg_coef,
                melody_audio, audio_prompt, progress_callback
            )
    
    def _generate_audiocraft(
        self, prompt, duration, temperature, top_k, top_p, cfg_coef,
        melody_audio, audio_prompt=None, progress_callback=None
    ):
        """Generate using audiocraft."""
        try:
            import torch
            
            # Check if this is a MAGNeT model (different API)
            model_id = MUSICGEN_MODELS.get(self.model_name, {}).get("id", "")
            is_magnet = "magnet" in model_id.lower()
            
            if is_magnet:
                # MAGNeT has fixed duration based on model config
                # and different generation params
                self.model.set_generation_params(
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p,
                )
                logger.info(f"MAGNeT model - using fixed duration of {getattr(self.model, 'duration', 30)}s")
            else:
                # MusicGen/AudioGen API
                self.model.set_generation_params(
                    duration=duration,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p,
                    cfg_coef=cfg_coef,
                )
            
            # 1. Melody Conditioning (structure)
            if melody_audio and MUSICGEN_MODELS[self.model_name]["melody"]:
                import torchaudio
                melody_waveform, sr = torchaudio.load(melody_audio)
                output = self.model.generate_with_chroma(
                    [prompt],
                    melody_waveform.unsqueeze(0),
                    sr,
                    progress=progress_callback is not None,
                )
            # 2. Audio Continuation (prompt)
            elif audio_prompt is not None:
                # Convert numpy prompt to torch tensor [B, C, T]
                # audio_prompt is likely [C, T] or [T] numpy array
                import torch
                
                if isinstance(audio_prompt, np.ndarray):
                    prompt_tensor = torch.from_numpy(audio_prompt)
                else:
                    prompt_tensor = audio_prompt
                    
                # Ensure dimensions [1, C, T] for batch 1
                if prompt_tensor.ndim == 1:
                    prompt_tensor = prompt_tensor.unsqueeze(0).unsqueeze(0)
                elif prompt_tensor.ndim == 2:
                     # Check if [C, T] or [T, C] - assume [C, T] as per librosa/standard
                     if prompt_tensor.shape[0] > 2 and prompt_tensor.shape[1] <= 2:
                         # Likely [T, C], transpose
                         prompt_tensor = prompt_tensor.t()
                     prompt_tensor = prompt_tensor.unsqueeze(0)
                
                # Check sample rate - we assume prompt is already at model SR (32k)
                # But audiocraft expects [B, C, T]
                
                logger.info(f"Using audio prompt for continuation: {prompt_tensor.shape}")
                
                output = self.model.generate_continuation(
                    prompt_tensor,
                    self.model.sample_rate,
                    [prompt],
                    progress=progress_callback is not None
                )
            # 3. Standard Text-to-Audio
            else:
                output = self.model.generate(
                    [prompt],
                    progress=progress_callback is not None,
                )
            
            audio = output[0].cpu().numpy()
            logger.info(f"Generated audio shape: {audio.shape}")
            return audio
            
        except Exception as e:
            logger.error(f"audiocraft generation failed: {e}")
            raise e
    
    def _generate_transformers(
        self, prompt, duration, temperature, top_k, top_p, cfg_coef,
        melody_audio=None, audio_prompt=None, progress_callback=None
    ):
        """Generate using Transformers."""
        try:
            import torch
            import numpy as np
            
            # Ensure model is on correct device
            device = self.model.device
            

                
            logger.info(f"Generating on {device}...")

            max_chunk_dur = get_config("max_chunk_duration", 30.0)
            
            # Use overlap for smoother transitions
            overlap_dur = get_config("overlap_duration", 0.5) # Duration to crossfade/overlap
            
            total_generated_audio = []
            
            remaining_duration = duration
            chunk_idx = 0
            
            last_chunk_audio = None
            
            while remaining_duration > 0:
                # We generate full chunks, but might trim the last one
                chunk_duration = min(remaining_duration, max_chunk_dur)
                logger.info(f"Generating chunk {chunk_idx+1}: {chunk_duration}s (Remaining: {remaining_duration}s)")
                
                # Determine prompt for this chunk
                current_prompt = prompt
                if isinstance(prompt, list):
                    if chunk_idx < len(prompt):
                        current_prompt = prompt[chunk_idx]
                    else:
                        current_prompt = prompt[-1]
                
                logger.info(f"Using prompt: '{current_prompt[:50]}...'")

                inputs = self.processor(
                    text=[current_prompt],
                    padding=True,
                    return_tensors="pt",
                ).to(device)
                
                # Handle audio prompt for continuation
                if last_chunk_audio is not None:
                    try:
                        # Prepare audio prompt from previous chunk
                        # Use last 10-15 seconds for best context
                        # MusicGen expects (samples,) but processor handles it
                        
                        proc_prompt = last_chunk_audio
                        
                        # Limit context length
                        max_ctx_sec = get_config("context_length_limit", 15.0) # seconds
                        max_samples = int(max_ctx_sec * self.sample_rate)
                        
                        if proc_prompt.shape[-1] > max_samples:
                            proc_prompt = proc_prompt[..., -max_samples:]
                            
                        # Ensure shape is right for processor
                        if len(proc_prompt.shape) == 2 and proc_prompt.shape[0] == 1:
                            proc_prompt = proc_prompt.flatten()
                        elif len(proc_prompt.shape) == 2 and proc_prompt.shape[0] > 1:
                             # Stereo to mono for conditioning (Models usually expect mono conditioning)
                             proc_prompt = proc_prompt.mean(axis=0)
                            
                        audio_inputs = self.processor(
                            audio=proc_prompt,
                            sampling_rate=self.sample_rate,
                            return_tensors="pt"
                        ).to(device)
                        
                        inputs["input_values"] = audio_inputs["input_values"]
                        if "padding_mask" in audio_inputs:
                            inputs["padding_mask"] = audio_inputs["padding_mask"]
                        
                    except Exception as e:
                        logger.warning(f"Failed to process audio prompt: {e}")

                # Calculate tokens
                # MusicGen generates 50 tokens per second
                tokens_per_sec = get_config("tokens_per_second", 50) 
                chunk_tokens = int(chunk_duration * tokens_per_sec)
                
                # If we have an audio prompt, we need to account for it in the context
                prompt_length_tokens = 0
                if "input_values" in inputs:
                     # Calculate how many tokens the prompt consumes
                     # 32000 samples -> 50 tokens (approx 640 samples per token)
                     audio_prompt_samples = inputs["input_values"].shape[-1]
                     magic_token_calc = get_config("magic_token_calc", 640)
                     prompt_length_tokens = int(audio_prompt_samples / magic_token_calc)
                     logger.info(f"Audio prompt length: {audio_prompt_samples} samples ({prompt_length_tokens} tokens)")

                # We want chunk_duration of NEW audio
                max_new_tokens = min(chunk_tokens, 1500 - prompt_length_tokens) 
                
                if max_new_tokens <= 0:
                    logger.warning("Context full! Cannot generate more tokens.")
                    break

                gen_kwargs = {
                    "max_new_tokens": max_new_tokens,
                    "do_sample": True,
                    "temperature": temperature,
                    "guidance_scale": cfg_coef,
                    "use_cache": True,  # Enforce dynamic KV caching
                }
                if top_k > 0: gen_kwargs["top_k"] = top_k
                if top_p > 0: gen_kwargs["top_p"] = top_p
                
                with torch.no_grad():
                    try:
                        # Disable SDPA hardware acceleration for DirectML compatibility
                        with torch.backends.cuda.sdp_kernel(enable_flash=False, enable_math=True, enable_mem_efficient=False):
                            audio_values = self.model.generate(**inputs, **gen_kwargs)
                    except Exception:
                        audio_values = self.model.generate(**inputs, **gen_kwargs)
                
                import gc
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                    torch.mps.empty_cache()
                
                # IMPORTANT: MusicGen's generate returns [Input + Generated]
                # If we provided an audio prompt, we must slice it off to get only the NEW audio
                chunk_audio_tensor = audio_values[0].cpu()
                
                if "input_values" in inputs:
                    # Slice off the input part
                    # The output length should be input_length + generated_length
                    # We might get slightly more or less due to frame sizes, so we use the prompt sample count
                    input_samples = inputs["input_values"].shape[-1]
                    if chunk_audio_tensor.shape[-1] > input_samples:
                        chunk_audio_tensor = chunk_audio_tensor[..., input_samples:]
                        logger.info(f"Sliced off {input_samples} samples of prompt. New audio: {chunk_audio_tensor.shape[-1]} samples")
                    else:
                        logger.warning("Output audio shorter than input prompt? Returning full output.")
                
                chunk_audio = chunk_audio_tensor.numpy()
                
                # Append to total with crossfade stitching
                if len(total_generated_audio) == 0:
                    total_generated_audio.append(chunk_audio)
                else:
                    # Crossfade stitching for smooth transitions
                    overlap_samples = int(overlap_dur * self.sample_rate)
                    prev = total_generated_audio[-1]
                    if overlap_samples > 0 and prev.shape[-1] >= overlap_samples and chunk_audio.shape[-1] >= overlap_samples:
                        fade_out = np.linspace(1.0, 0.0, overlap_samples)
                        fade_in = np.linspace(0.0, 1.0, overlap_samples)
                        if prev.ndim == 2:
                            fade_out = fade_out[np.newaxis, :]
                            fade_in = fade_in[np.newaxis, :]
                        blended = prev[..., -overlap_samples:] * fade_out + chunk_audio[..., :overlap_samples] * fade_in
                        total_generated_audio[-1] = prev[..., :-overlap_samples]
                        total_generated_audio.append(blended)
                        total_generated_audio.append(chunk_audio[..., overlap_samples:])
                    else:
                        total_generated_audio.append(chunk_audio)

                # Setup for next chunk (use the NEW audio as prompt for next)
                last_chunk_audio = chunk_audio
                remaining_duration -= chunk_duration
                chunk_idx += 1
                
                if progress_callback:
                    progress_callback(duration - remaining_duration, duration)

            # Concatenate all chunks and handle potentially 1D or 2D arrays
            processed_chunks = []
            for chunk in total_generated_audio:
                if chunk.ndim == 1:
                    chunk = chunk[np.newaxis, :]
                processed_chunks.append(chunk)

            full_audio = np.concatenate(processed_chunks, axis=-1)
            
            logger.info(f"Total generated audio shape: {full_audio.shape}")
            return full_audio
            
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            logger.error(f"Transformers generation failed: {str(e)}\n{tb}")
            raise e
    
    def unload(self) -> None:
        """Unload model and free memory."""
        logger.info("Unloading MusicGen model...")
        if self.model is not None:
            import gc
            import torch
            del self.model
            self.model = None
            if self.processor is not None:
                del self.processor
                self.processor = None
            
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            self.model_name = None
            self.backend = LoaderBackend.NONE
            logger.info("MusicGen model unloaded.")




def list_models():
    """Print available models to console."""
    logger.info("\n╔════════════════════════════════════════════════════════════╗")
    logger.info("║  Available MusicGen Models                                 ║")
    logger.info("╠════════════════════════════════════════════════════════════╣")
    for name, info in MUSICGEN_MODELS.items():
        stereo = "✓" if info["stereo"] else " "
        melody = "✓" if info["melody"] else " "
        logger.info(f"║  {name:<14} {info['params']:>5}  {info['vram_gb']:>2}GB  Stereo:{stereo}  Melody:{melody}  ║")
    logger.info("╚════════════════════════════════════════════════════════════╝\n")


if __name__ == "__main__":
    list_models()
