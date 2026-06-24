"""
Kraftbeat Streaming Generation

Generate audio incrementally and play as it generates.
Provides callback-based streaming for real-time playback.
"""

import logging
import threading
from typing import Optional, Callable, Generator
import numpy as np

logger = logging.getLogger(__name__)

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False


class StreamingGenerator:
    """
    Generate audio in chunks and stream to playback.
    
    Usage:
        streamer = StreamingGenerator(model, sample_rate=32000)
        streamer.start_streaming("epic orchestral music", on_chunk=callback)
    """
    
    def __init__(
        self,
        model,
        sample_rate: int = 32000,
        chunk_duration: float = 2.0,  # seconds per chunk
    ):
        self.model = model
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.chunk_samples = int(sample_rate * chunk_duration)
        
        self.is_streaming = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # Audio buffer for playback
        self.audio_buffer = []
        self.stream: Optional[sd.OutputStream] = None
    
    def start_streaming(
        self,
        prompt: str,
        total_duration: float = 30.0,
        on_chunk: Optional[Callable[[np.ndarray, int], None]] = None,
        on_complete: Optional[Callable[[np.ndarray], None]] = None,
        play_audio: bool = True,
    ) -> bool:
        """
        Start streaming generation.
        
        Args:
            prompt: Generation prompt
            total_duration: Total duration to generate
            on_chunk: Callback for each chunk (audio, chunk_index)
            on_complete: Callback when complete (full_audio)
            play_audio: Whether to play audio as it generates
            
        Returns:
            True if started successfully
        """
        if self.is_streaming:
            logger.warning("Already streaming")
            return False
        
        self._stop_event.clear()
        self.audio_buffer = []
        self.is_streaming = True
        
        def generate_thread():
            try:
                total_samples = int(total_duration * self.sample_rate)
                generated_samples = 0
                chunk_index = 0
                all_audio = []
                
                # Start audio output stream if requested
                if play_audio and AUDIO_AVAILABLE:
                    self.stream = sd.OutputStream(
                        samplerate=self.sample_rate,
                        channels=1,
                        dtype=np.float32,
                    )
                    self.stream.start()
                
                while generated_samples < total_samples and not self._stop_event.is_set():
                    # Generate chunk
                    remaining = min(self.chunk_duration, (total_samples - generated_samples) / self.sample_rate)
                    
                    logger.info(f"Generating chunk {chunk_index + 1} ({remaining:.1f}s)...")
                    
                    # Generate using continuation if we have previous audio
                    if all_audio:
                        # Use last bit as context for continuation
                        context = np.concatenate(all_audio)[-self.sample_rate:]
                        chunk = self._generate_chunk(prompt, remaining, context)
                    else:
                        chunk = self._generate_chunk(prompt, remaining)
                    
                    if chunk is None:
                        break
                    
                    all_audio.append(chunk)
                    generated_samples += len(chunk)
                    
                    # Play chunk
                    if play_audio and self.stream:
                        if chunk.ndim > 1:
                            chunk_mono = chunk.mean(axis=0)
                        else:
                            chunk_mono = chunk
                        self.stream.write(chunk_mono.astype(np.float32))
                    
                    # Callback
                    if on_chunk:
                        on_chunk(chunk, chunk_index)
                    
                    chunk_index += 1
                
                # Complete
                full_audio = np.concatenate(all_audio) if all_audio else np.array([])
                
                if on_complete:
                    on_complete(full_audio)
                
                logger.info(f"Streaming complete: {len(full_audio)/self.sample_rate:.1f}s")
                
            except Exception as e:
                logger.error(f"Streaming error: {e}")
            finally:
                self.is_streaming = False
                if self.stream:
                    self.stream.stop()
                    self.stream.close()
                    self.stream = None
        
        self._thread = threading.Thread(target=generate_thread, daemon=True)
        self._thread.start()
        return True
    
    def stop_streaming(self):
        """Stop streaming generation."""
        self._stop_event.set()
        self.is_streaming = False
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
    
    def _generate_chunk(
        self,
        prompt: str,
        duration: float,
        context: Optional[np.ndarray] = None,
    ) -> Optional[np.ndarray]:
        """Generate a single chunk of audio."""
        
        if not TORCH_AVAILABLE:
            return None
        
        try:
            with torch.no_grad():
                if hasattr(self.model, 'generate'):
                    gen_kwargs = {
                        'descriptions': [prompt],
                        'progress': False,
                    }
                    
                    # Pass duration if model supports it
                    if hasattr(self.model, 'set_generation_params'):
                        self.model.set_generation_params(duration=duration)
                    
                    # Use context for continuation if available
                    if context is not None:
                        context_tensor = torch.from_numpy(context).float()
                        if context_tensor.ndim == 1:
                            context_tensor = context_tensor.unsqueeze(0).unsqueeze(0)
                        elif context_tensor.ndim == 2:
                            context_tensor = context_tensor.unsqueeze(0)
                        gen_kwargs['melody_wavs'] = context_tensor
                        gen_kwargs['melody_sample_rate'] = self.sample_rate
                    
                    audio = self.model.generate(**gen_kwargs)
                    return audio[0].cpu().numpy()
                else:
                    logger.warning("Model doesn't support generate()")
                    return None
                    
        except Exception as e:
            logger.error(f"Chunk generation failed: {e}")
            return None


def create_stream_callback(
    on_progress: Callable[[float], None],
    on_waveform: Callable[[np.ndarray], None],
    sample_rate: int = 32000,
    total_duration: float = 30.0,
) -> Callable[[np.ndarray, int], None]:
    """
    Create a streaming callback for UI updates.
    
    Args:
        on_progress: Progress callback (0.0 to 1.0)
        on_waveform: Waveform update callback
        sample_rate: Audio sample rate
        total_duration: Total expected duration in seconds
        
    Returns:
        Chunk callback function
    """
    all_chunks = []
    total_samples = sample_rate * total_duration
    
    def on_chunk(chunk: np.ndarray, index: int):
        all_chunks.append(chunk)
        full_audio = np.concatenate(all_chunks)
        
        on_waveform(full_audio)
        on_progress(min(1.0, len(full_audio) / total_samples))
    
    return on_chunk
