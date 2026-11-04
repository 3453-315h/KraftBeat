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
) -> Optional[str]:
    """
    Save audio array to file.
    
    Args:
        audio: Audio data as numpy array (channels, samples) or (samples,)
        filepath: Output file path
        sample_rate: Audio sample rate
        audio_format: Output format (wav, mp3, flac, ogg)
        bitrate: Bitrate for lossy formats (e.g., "128k", "192k", "320k")
        
    Returns:
        Path string to saved audio if successful, None otherwise
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
        fmt = audio_format.lower()
        if filepath.suffix.lower() != f".{fmt}":
            filepath = filepath.with_suffix(f".{fmt}")
        
        # WAV and FLAC use soundfile directly
        if fmt in ("wav", "flac"):
            sf.write(str(filepath), audio, sample_rate)
            logger.info(f"Saved audio to: {filepath}")
            return str(filepath)
        
        # MP3 and OGG need pydub
        if fmt in ("mp3", "ogg"):
            temp_wav = filepath.with_suffix(".temp.wav")
            try:
                from pydub import AudioSegment
                
                # Save temp WAV first
                sf.write(str(temp_wav), audio, sample_rate)
                
                # Convert with pydub
                audio_segment = AudioSegment.from_wav(str(temp_wav))
                audio_segment.export(
                    str(filepath),
                    format=fmt,
                    bitrate=bitrate
                )
                logger.info(f"Saved audio to: {filepath} ({bitrate})")
                return str(filepath)
                
            except ImportError:
                logger.warning("pydub not installed, falling back to WAV")
                filepath = filepath.with_suffix(".wav")
                sf.write(str(filepath), audio, sample_rate)
                return str(filepath)
            except Exception as e:
                logger.error(f"pydub export error (ffmpeg missing or invalid): {e}; falling back to WAV")
                filepath = filepath.with_suffix(".wav")
                sf.write(str(filepath), audio, sample_rate)
                return str(filepath)
            finally:
                if temp_wav.exists():
                    try:
                        temp_wav.unlink()
                    except OSError:
                        pass
        
        # Fallback to WAV
        sf.write(str(filepath), audio, sample_rate)
        logger.info(f"Saved audio to: {filepath}")
        return str(filepath)
        
    except Exception as e:
        logger.error(f"Failed to save audio: {e}")
        return None


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


def crossfade_audio(
    audio1: np.ndarray,
    audio2: np.ndarray,
    crossfade_samples: int,
    curve: str = "equal_power",
) -> np.ndarray:
    """
    Seamlessly crossfade and concatenate two audio arrays.
    
    Supports 1D (samples,) and 2D arrays ((channels, samples) or (samples, channels)).
    Maintains input orientation and normalizes channel counts if one is mono and one is stereo.
    
    Args:
        audio1: First audio segment
        audio2: Second audio segment
        crossfade_samples: Overlap duration in samples
        curve: 'equal_power' (avoids volume dip) or 'linear'
        
    Returns:
        Concatenated and crossfaded numpy audio array.
    """
    if audio1 is None or len(audio1) == 0:
        return audio2 if audio2 is not None else np.array([], dtype=np.float32)
    if audio2 is None or len(audio2) == 0:
        return audio1

    orig_1d = (audio1.ndim == 1 and audio2.ndim == 1)
    
    a1 = np.asarray(audio1)
    a2 = np.asarray(audio2)

    if orig_1d:
        s1 = len(a1)
        s2 = len(a2)
        if crossfade_samples <= 0 or crossfade_samples >= s1 or crossfade_samples >= s2:
            return np.concatenate([a1, a2])

        if curve == "equal_power":
            t = np.linspace(0.0, np.pi / 2, crossfade_samples, dtype=np.float32)
            fade_out = np.cos(t)
            fade_in = np.sin(t)
        else:
            fade_out = np.linspace(1.0, 0.0, crossfade_samples, dtype=np.float32)
            fade_in = np.linspace(0.0, 1.0, crossfade_samples, dtype=np.float32)

        overlap = a1[-crossfade_samples:] * fade_out + a2[:crossfade_samples] * fade_in
        return np.concatenate([a1[:-crossfade_samples], overlap, a2[crossfade_samples:]])

    # 2D handling: normalize orientation to (channels, samples)
    transposed_1 = False
    if a1.ndim == 1:
        a1 = a1[np.newaxis, :]
    elif a1.ndim == 2 and (a1.shape[0] > 8 or a1.shape[0] >= a1.shape[1]):
        a1 = a1.T
        transposed_1 = True

    if a2.ndim == 1:
        a2 = a2[np.newaxis, :]
    elif a2.ndim == 2 and (a2.shape[0] > 8 or a2.shape[0] >= a2.shape[1]):
        a2 = a2.T

    # Align channel count: mono to stereo if needed
    if a1.shape[0] == 1 and a2.shape[0] > 1:
        a1 = np.repeat(a1, a2.shape[0], axis=0)
    elif a2.shape[0] == 1 and a1.shape[0] > 1:
        a2 = np.repeat(a2, a1.shape[0], axis=0)

    s1 = a1.shape[1]
    s2 = a2.shape[1]

    if crossfade_samples <= 0 or crossfade_samples >= s1 or crossfade_samples >= s2:
        res = np.concatenate([a1, a2], axis=1)
        return res.T if transposed_1 else res

    if curve == "equal_power":
        t = np.linspace(0.0, np.pi / 2, crossfade_samples, dtype=np.float32)
        fade_out = np.cos(t)[np.newaxis, :]
        fade_in = np.sin(t)[np.newaxis, :]
    else:
        fade_out = np.linspace(1.0, 0.0, crossfade_samples, dtype=np.float32)[np.newaxis, :]
        fade_in = np.linspace(0.0, 1.0, crossfade_samples, dtype=np.float32)[np.newaxis, :]

    overlap = a1[:, -crossfade_samples:] * fade_out + a2[:, :crossfade_samples] * fade_in
    res = np.concatenate([a1[:, :-crossfade_samples], overlap, a2[:, crossfade_samples:]], axis=1)

    return res.T if transposed_1 else res
