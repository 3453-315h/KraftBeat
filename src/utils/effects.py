"""
Kraftbeat Audio Effects

Post-processing effects chain for polishing generated audio.
Uses scipy for basic DSP and optionally pedalboard for pro effects.
"""

import logging
from typing import Optional
import numpy as np

logger = logging.getLogger(__name__)


def apply_reverb(
    audio: np.ndarray,
    sample_rate: int,
    room_size: float = 0.5,
    wet: float = 0.3,
) -> np.ndarray:
    """
    Apply reverb effect using convolution.
    
    Args:
        audio: Input audio array
        sample_rate: Audio sample rate
        room_size: Room size (0.0-1.0)
        wet: Wet/dry mix (0.0-1.0)
        
    Returns:
        Audio with reverb applied
    """
    if wet <= 0:
        return audio
    
    try:
        from scipy import signal
        
        # Create impulse response (simple exponential decay)
        ir_length = int(sample_rate * room_size * 2)  # Up to 2 seconds
        ir = np.exp(-np.linspace(0, 8, ir_length))
        ir = ir / np.sum(ir)  # Normalize
        
        # Handle stereo
        if audio.ndim == 1:
            reverbed = signal.convolve(audio, ir, mode='same')
        else:
            reverbed = np.array([
                signal.convolve(ch, ir, mode='same') 
                for ch in audio
            ])
        
        # Mix dry/wet
        return audio * (1 - wet) + reverbed * wet
        
    except Exception as e:
        logger.warning(f"Reverb failed: {e}")
        return audio


def apply_compression(
    audio: np.ndarray,
    threshold_db: float = -20.0,
    ratio: float = 4.0,
    attack_ms: float = 10.0,
    release_ms: float = 100.0,
    sample_rate: int = 32000,
) -> np.ndarray:
    """
    Apply dynamic range compression.
    
    Args:
        audio: Input audio array
        threshold_db: Threshold in dB
        ratio: Compression ratio (4:1 = heavy compression)
        attack_ms: Attack time in milliseconds
        release_ms: Release time in milliseconds
        sample_rate: Audio sample rate
        
    Returns:
        Compressed audio
    """
    if ratio <= 1.0:
        return audio
    
    try:
        threshold = 10 ** (threshold_db / 20)
        
        # Get envelope
        abs_audio = np.abs(audio)
        if audio.ndim > 1:
            envelope = np.max(abs_audio, axis=0)
        else:
            envelope = abs_audio
        
        # Calculate gain reduction
        gain = np.ones_like(envelope)
        above_thresh = envelope > threshold
        gain[above_thresh] = threshold + (envelope[above_thresh] - threshold) / ratio
        gain = gain / np.maximum(envelope, 1e-10)
        
        # Simple smoothing (attack/release approximation)
        from scipy.ndimage import uniform_filter1d
        smooth_samples = int(sample_rate * attack_ms / 1000)
        if smooth_samples > 1:
            gain = uniform_filter1d(gain, smooth_samples)
        
        # Apply gain
        if audio.ndim > 1:
            return audio * gain
        return audio * gain
        
    except Exception as e:
        logger.warning(f"Compression failed: {e}")
        return audio


def apply_eq(
    audio: np.ndarray,
    sample_rate: int,
    bass_db: float = 0.0,
    mid_db: float = 0.0,
    treble_db: float = 0.0,
) -> np.ndarray:
    """
    Apply 3-band equalizer.
    
    Args:
        audio: Input audio array
        sample_rate: Audio sample rate
        bass_db: Bass gain in dB (< 200 Hz)
        mid_db: Mid gain in dB (200 Hz - 2 kHz)
        treble_db: Treble gain in dB (> 2 kHz)
        
    Returns:
        EQ'd audio
    """
    if bass_db == 0 and mid_db == 0 and treble_db == 0:
        return audio
    
    try:
        from scipy import signal
        
        nyquist = sample_rate / 2
        
        # Band definitions
        bass_cutoff = 200 / nyquist
        mid_cutoff = 2000 / nyquist
        
        # Ensure valid frequencies
        bass_cutoff = min(0.99, max(0.01, bass_cutoff))
        mid_cutoff = min(0.99, max(0.01, mid_cutoff))
        
        result = np.zeros_like(audio, dtype=float)
        
        # Bass (lowpass)
        b_lo, a_lo = signal.butter(2, bass_cutoff, btype='low')
        bass = signal.filtfilt(b_lo, a_lo, audio, axis=-1)
        result += bass * (10 ** (bass_db / 20))
        
        # Mid (bandpass)
        b_mid, a_mid = signal.butter(2, [bass_cutoff, mid_cutoff], btype='band')
        mid = signal.filtfilt(b_mid, a_mid, audio, axis=-1)
        result += mid * (10 ** (mid_db / 20))
        
        # Treble (highpass)
        b_hi, a_hi = signal.butter(2, mid_cutoff, btype='high')
        treble = signal.filtfilt(b_hi, a_hi, audio, axis=-1)
        result += treble * (10 ** (treble_db / 20))
        
        return result
        
    except Exception as e:
        logger.warning(f"EQ failed: {e}")
        return audio


def apply_limiter(
    audio: np.ndarray,
    ceiling_db: float = -1.0,
) -> np.ndarray:
    """
    Apply brick-wall limiter.
    
    Args:
        audio: Input audio array
        ceiling_db: Maximum output level in dB
        
    Returns:
        Limited audio
    """
    ceiling = 10 ** (ceiling_db / 20)
    return np.clip(audio, -ceiling, ceiling)


def apply_stereo_width(
    audio: np.ndarray,
    width: float = 1.0,
) -> np.ndarray:
    """
    Adjust stereo width.
    
    Args:
        audio: Input audio array (2, samples) for stereo
        width: Width factor (0.0 = mono, 1.0 = normal, 2.0 = extra wide)
        
    Returns:
        Audio with adjusted stereo width
    """
    if audio.ndim != 2 or audio.shape[0] != 2:
        return audio  # Not stereo
    
    if width == 1.0:
        return audio
    
    # Mid-side processing
    mid = (audio[0] + audio[1]) / 2
    side = (audio[0] - audio[1]) / 2
    
    # Adjust width
    side = side * width
    
    # Convert back to L/R
    left = mid + side
    right = mid - side
    
    return np.array([left, right])


def apply_effects_chain(
    audio: np.ndarray,
    sample_rate: int,
    reverb_wet: float = 0.0,
    reverb_room: float = 0.5,
    compression_ratio: float = 1.0,
    compression_threshold: float = -20.0,
    eq_bass: float = 0.0,
    eq_mid: float = 0.0,
    eq_treble: float = 0.0,
    stereo_width: float = 1.0,
    limiter_ceiling: float = -1.0,
) -> np.ndarray:
    """
    Apply full effects chain in optimal order.
    
    Order: EQ -> Compression -> Reverb -> Stereo -> Limiter
    """
    # EQ first (shape the tone)
    audio = apply_eq(audio, sample_rate, eq_bass, eq_mid, eq_treble)
    
    # Compression (control dynamics)
    audio = apply_compression(
        audio, 
        threshold_db=compression_threshold,
        ratio=compression_ratio,
        sample_rate=sample_rate
    )
    
    # Reverb (add space)
    audio = apply_reverb(audio, sample_rate, reverb_room, reverb_wet)
    
    # Stereo width
    audio = apply_stereo_width(audio, stereo_width)
    
    # Limiter last (prevent clipping)
    audio = apply_limiter(audio, limiter_ceiling)
    
    return audio
