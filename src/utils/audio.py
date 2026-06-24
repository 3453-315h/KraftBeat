"""
Kraftbeat Audio Utilities

Audio file I/O and processing helpers.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)


def save_audio(
    audio: np.ndarray,
    filepath: str,
    sample_rate: int = 32000,
    audio_format: str = "wav",
    bitrate: str = "192k",
) -> bool:
    """
    Save audio array to file.
    
    Args:
        audio: Audio data as numpy array (channels, samples) or (samples,)
        filepath: Output file path
        sample_rate: Audio sample rate
        audio_format: Output format (wav, mp3, flac, ogg)
        bitrate: Bitrate for lossy formats (e.g., "128k", "192k", "320k")
        
    Returns:
        True if successful
    """
    try:
        import soundfile as sf
        
        # Ensure correct shape (samples, channels)
        if audio.ndim == 1:
            audio = audio.reshape(-1, 1)
        elif audio.ndim == 2 and audio.shape[0] <= 8 and audio.shape[0] < audio.shape[1]:
            # Only transpose if first dim looks like channels (<=8) and is smaller
            audio = audio.T
        
        # Ensure proper file extension
        filepath = Path(filepath)
        if filepath.suffix.lower() != f".{audio_format}":
            filepath = filepath.with_suffix(f".{audio_format}")
        
        # WAV and FLAC use soundfile directly
        if audio_format.lower() in ("wav", "flac"):
            sf.write(str(filepath), audio, sample_rate)
            logger.info(f"Saved audio to: {filepath}")
            return True
        
        # MP3 and OGG need pydub
        if audio_format.lower() in ("mp3", "ogg"):
            try:
                from pydub import AudioSegment
                
                # Save temp WAV first
                temp_wav = filepath.with_suffix(".temp.wav")
                sf.write(str(temp_wav), audio, sample_rate)
                
                # Convert with pydub
                audio_segment = AudioSegment.from_wav(str(temp_wav))
                audio_segment.export(
                    str(filepath),
                    format=audio_format.lower(),
                    bitrate=bitrate
                )
                
                # Cleanup temp file
                temp_wav.unlink()
                logger.info(f"Saved audio to: {filepath} ({bitrate})")
                return True
                
            except ImportError:
                logger.warning("pydub not installed, falling back to WAV")
                filepath = filepath.with_suffix(".wav")
                sf.write(str(filepath), audio, sample_rate)
                return True
            except Exception as e:
                logger.error(f"pydub error (ffmpeg installed?): {e}")
                filepath = filepath.with_suffix(".wav")
                sf.write(str(filepath), audio, sample_rate)
                return True
        
        # Fallback to WAV
        sf.write(str(filepath), audio, sample_rate)
        logger.info(f"Saved audio to: {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save audio: {e}")
        return False


def load_audio(
    filepath: str,
    target_sr: Optional[int] = None,
) -> Optional[Tuple[np.ndarray, int]]:
    """
    Load audio file.
    
    Args:
        filepath: Path to audio file
        target_sr: Optional target sample rate for resampling
        
    Returns:
        Tuple of (audio_array, sample_rate) or None on failure
    """
    try:
        import soundfile as sf
        
        audio, sr = sf.read(filepath)
        
        if target_sr and sr != target_sr:
            from scipy import signal
            # Compute correct number of output samples based on total sample count
            # For multi-channel audio (samples, channels), audio.shape[0] gives sample count
            num_samples = int(audio.shape[0] * target_sr / sr)
            audio = signal.resample(audio, num_samples)
            sr = target_sr
        
        return audio, sr
        
    except Exception as e:
        logger.error(f"Failed to load audio: {e}")
        return None


def get_duration(audio: np.ndarray, sample_rate: int) -> float:
    """Calculate audio duration in seconds."""
    if audio.ndim == 1:
        return len(audio) / sample_rate
    # To handle both (channels, samples) and (samples, channels) reliably:
    return max(audio.shape) / sample_rate


def normalize_audio(audio: np.ndarray, target_db: float = -3.0) -> np.ndarray:
    """
    Normalize audio to target dB level.
    
    Args:
        audio: Input audio array
        target_db: Target peak level in dB (default -3dB for headroom)
        
    Returns:
        Normalized audio
    """
    peak = np.abs(audio).max()
    if peak > 0:
        target_linear = 10 ** (target_db / 20)
        audio = audio * (target_linear / peak)
    return audio
