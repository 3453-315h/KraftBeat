"""
Kraftbeat Stem Separation

Split audio into stems using Demucs (drums, bass, vocals, other).
Requires: pip install demucs
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Tuple
import numpy as np

logger = logging.getLogger(__name__)

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# Check for demucs
DEMUCS_AVAILABLE = False
try:
    from demucs import pretrained
    from demucs.apply import apply_model
    DEMUCS_AVAILABLE = True
except ImportError:
    logger.info("Demucs not installed - stem separation unavailable")


STEM_NAMES = ["drums", "bass", "other", "vocals"]


def separate_stems(
    audio: np.ndarray,
    sample_rate: int = 44100,
    model_name: str = "htdemucs",
    device: str = "auto",
) -> Optional[Dict[str, np.ndarray]]:
    """
    Separate audio into stems.
    
    Args:
        audio: Audio array (samples,) or (channels, samples)
        sample_rate: Audio sample rate
        model_name: Demucs model name (htdemucs, htdemucs_ft, etc.)
        device: Compute device (auto, cuda, cpu)
        
    Returns:
        Dict of stem_name -> audio_array, or None on failure
    """
    if not DEMUCS_AVAILABLE:
        logger.error("Demucs not installed. Run: pip install demucs")
        return None
    
    if not TORCH_AVAILABLE:
        logger.error("PyTorch not available")
        return None
    
    try:
        # Determine device
        if device == "auto":
            if torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"
        
        logger.info(f"Loading Demucs model: {model_name}")
        model = pretrained.get_model(model_name)
        model.to(device)
        model.eval()
        
        # Prepare audio tensor
        if audio.ndim == 1:
            audio = np.stack([audio, audio])  # Mono to stereo
        
        # Ensure (channels, samples)
        if audio.shape[0] > audio.shape[1]:
            audio = audio.T
        
        # Convert to tensor
        audio_tensor = torch.from_numpy(audio).float()
        
        # Add batch dimension
        audio_tensor = audio_tensor.unsqueeze(0).to(device)
        
        # Resample if needed (Demucs expects 44100 Hz)
        if sample_rate != model.samplerate:
            from torchaudio.transforms import Resample
            resampler = Resample(sample_rate, model.samplerate).to(device)
            audio_tensor = resampler(audio_tensor)
        
        logger.info("Separating stems...")
        with torch.no_grad():
            sources = apply_model(model, audio_tensor, device=device)
        
        # Convert to numpy
        sources = sources[0].cpu().numpy()  # Remove batch dim
        
        # Build result dict
        stems = {}
        for i, name in enumerate(model.sources):
            stems[name] = sources[i]  # (channels, samples)
        
        logger.info(f"Separated into {len(stems)} stems: {list(stems.keys())}")
        return stems
        
    except Exception as e:
        logger.error(f"Stem separation failed: {e}")
        return None


def save_stems(
    stems: Dict[str, np.ndarray],
    output_dir: str,
    sample_rate: int = 44100,
    audio_format: str = "wav",
) -> Dict[str, str]:
    """
    Save stems to files.
    
    Args:
        stems: Dict of stem_name -> audio_array
        output_dir: Output directory
        sample_rate: Audio sample rate
        format: Output format (wav, mp3, flac)
        
    Returns:
        Dict of stem_name -> file_path
    """
    from src.utils.audio import save_audio
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    saved = {}
    for name, audio in stems.items():
        filepath = output_dir / f"{name}.{audio_format}"
        if save_audio(audio, str(filepath), sample_rate, audio_format):
            saved[name] = str(filepath)
            logger.info(f"Saved: {filepath}")
    
    return saved


def separate_file(
    input_path: str,
    output_dir: Optional[str] = None,
    model_name: str = "htdemucs",
) -> Optional[Dict[str, str]]:
    """
    Separate a file into stems.
    
    Args:
        input_path: Input audio file path
        output_dir: Output directory (default: same as input)
        model_name: Demucs model name
        
    Returns:
        Dict of stem_name -> file_path, or None on failure
    """
    from src.utils.audio import load_audio
    
    # Load audio
    result = load_audio(input_path)
    if result is None:
        return None
    
    audio, sr = result
    
    # Separate
    stems = separate_stems(audio, sr, model_name)
    if stems is None:
        return None
    
    # Save
    if output_dir is None:
        output_dir = Path(input_path).parent / Path(input_path).stem
    
    return save_stems(stems, output_dir, sr)


def get_available_models() -> list:
    """Get list of available Demucs models."""
    return [
        {"name": "htdemucs", "desc": "Default model, good quality"},
        {"name": "htdemucs_ft", "desc": "Fine-tuned, better quality"},
        {"name": "htdemucs_6s", "desc": "6 stems (adds piano, guitar)"},
        {"name": "mdx_extra", "desc": "MDX competition winner"},
    ]
