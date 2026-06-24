"""
Kraftbeat Audio Recorder

Record audio from microphone for melody conditioning.
Uses sounddevice for cross-platform audio input.
"""

import logging
import threading
from typing import Optional, Callable
import numpy as np

logger = logging.getLogger(__name__)

try:
    import sounddevice as sd
    RECORDING_AVAILABLE = True
except ImportError:
    RECORDING_AVAILABLE = False
    logger.warning("sounddevice not available - recording disabled")


class AudioRecorder:
    """
    Record audio from microphone.
    
    Usage:
        recorder = AudioRecorder()
        recorder.start_recording(callback=on_audio_ready)
        # ... user records ...
        recorder.stop_recording()
    """
    
    def __init__(
        self,
        sample_rate: int = 32000,
        channels: int = 1,
        max_duration: float = 30.0,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.max_duration = max_duration
        
        self.is_recording = False
        self.audio_buffer: list = []
        self.stream: Optional[sd.InputStream] = None
        self._callback: Optional[Callable] = None
        self._stop_event = threading.Event()
        
    def start_recording(
        self,
        callback: Optional[Callable[[np.ndarray, int], None]] = None,
    ) -> bool:
        """
        Start recording from microphone.
        
        Args:
            callback: Function called with (audio_array, sample_rate) when done
            
        Returns:
            True if recording started successfully
        """
        if not RECORDING_AVAILABLE:
            logger.error("Recording not available - sounddevice not installed")
            return False
            
        if self.is_recording:
            logger.warning("Already recording")
            return False
        
        self._callback = callback
        self.audio_buffer = []
        self._stop_event.clear()
        
        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self._audio_callback,
                dtype=np.float32,
            )
            self.stream.start()
            self.is_recording = True
            logger.info(f"🎤 Recording started (max {self.max_duration}s)")
            
            # Auto-stop timer
            self._timer = threading.Timer(self.max_duration, self.stop_recording)
            self._timer.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            return False
    
    def _audio_callback(self, indata, frames, time, status):
        """Handle incoming audio data."""
        if status:
            logger.warning(f"Recording status: {status}")
        
        if self.is_recording:
            self.audio_buffer.append(indata.copy())
    
    def stop_recording(self) -> Optional[np.ndarray]:
        """
        Stop recording and return the audio.
        
        Returns:
            Audio array or None if no recording
        """
        if not self.is_recording:
            return None
        
        self.is_recording = False
        self._stop_event.set()
        
        # Cancel timer
        if hasattr(self, '_timer'):
            self._timer.cancel()
        
        # Stop stream
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        # Combine buffer
        if not self.audio_buffer:
            return None
        
        audio = np.concatenate(self.audio_buffer, axis=0)
        audio = audio.flatten()  # Mono
        
        duration = len(audio) / self.sample_rate
        logger.info(f"🎤 Recording stopped: {duration:.1f}s")
        
        # Call callback if provided
        if self._callback:
            self._callback(audio, self.sample_rate)
        
        return audio
    
    def get_input_devices(self) -> list:
        """Get list of available input devices."""
        if not RECORDING_AVAILABLE:
            return []
        
        devices = []
        try:
            for i, device in enumerate(sd.query_devices()):
                if device['max_input_channels'] > 0:
                    devices.append({
                        'index': i,
                        'name': device['name'],
                        'channels': device['max_input_channels'],
                        'sample_rate': device['default_samplerate'],
                    })
        except Exception as e:
            logger.error(f"Failed to list devices: {e}")
        
        return devices


def record_melody(duration: float = 10.0) -> Optional[np.ndarray]:
    """
    Simple blocking function to record melody.
    
    Args:
        duration: Recording duration in seconds
        
    Returns:
        Audio array or None
    """
    if not RECORDING_AVAILABLE:
        return None
    
    logger.info(f"🎤 Recording for {duration}s... Press Ctrl+C to stop early")
    
    try:
        audio = sd.rec(
            int(duration * 32000),
            samplerate=32000,
            channels=1,
            dtype=np.float32,
        )
        sd.wait()
        return audio.flatten()
    except KeyboardInterrupt:
        sd.stop()
        return None
    except Exception as e:
        logger.error(f"Recording failed: {e}")
        return None
