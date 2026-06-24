"""
Kraftbeat Performance Utilities

Memory profiling, GPU monitoring, thread pooling, and resource optimization.
"""

import logging
import sys
import gc
import os
from typing import Optional, Dict, Callable, Any, List
from dataclasses import dataclass, replace as dataclass_replace
from concurrent.futures import ThreadPoolExecutor, Future
from threading import Lock
import queue

logger = logging.getLogger(__name__)

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


@dataclass
class MemoryStats:
    """Memory usage statistics."""
    ram_used: int  # bytes
    ram_total: int
    ram_percent: float
    vram_used: int = 0
    vram_total: int = 0
    vram_percent: float = 0.0
    device_name: str = "CPU"


@dataclass
class PerformanceSettings:
    """Performance configuration."""
    num_workers: int = 4
    pool_size: int = 4
    torch_threads: int = 4
    batch_size: int = 1
    parallel_effects: bool = True
    async_save: bool = True
    lazy_loading: bool = True
    model_unload_timeout: int = 10  # minutes
    gc_on_generate: bool = False
    clear_cache_between: bool = False


# Global performance settings
_settings = PerformanceSettings()
_settings_lock = Lock()


def get_settings() -> PerformanceSettings:
    """Get current performance settings (returns a copy)."""
    with _settings_lock:
        return dataclass_replace(_settings)


def update_settings(**kwargs):
    """Update performance settings."""
    global _settings
    with _settings_lock:
        for key, value in kwargs.items():
            if hasattr(_settings, key):
                setattr(_settings, key, value)
                logger.info(f"Performance setting updated: {key} = {value}")
    
    # Apply PyTorch thread count if changed
    if 'torch_threads' in kwargs and TORCH_AVAILABLE:
        torch.set_num_threads(kwargs['torch_threads'])
        logger.info(f"PyTorch threads set to {kwargs['torch_threads']}")


class ThreadPoolManager:
    """
    Manages thread pools for background tasks.
    
    Singleton pattern - use get_pool() to access.
    """
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._executor: Optional[ThreadPoolExecutor] = None
        self._pool_size = 4
        self._pending_futures: List[Future] = []
        self._task_queue = queue.Queue()
        
        logger.info("ThreadPoolManager initialized")
    
    def start(self, pool_size: int = None):
        """Start the thread pool with specified size."""
        if pool_size is None:
            pool_size = get_settings().pool_size
        
        if self._executor is not None:
            self.shutdown()
        
        self._pool_size = pool_size
        self._executor = ThreadPoolExecutor(
            max_workers=pool_size,
            thread_name_prefix="kraftbeat_worker"
        )
        logger.info(f"Thread pool started with {pool_size} workers")
    
    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        """Submit a task to the thread pool."""
        if self._executor is None:
            self.start()
        
        future = self._executor.submit(fn, *args, **kwargs)
        self._pending_futures.append(future)
        
        # Clean up completed futures
        self._pending_futures = [f for f in self._pending_futures if not f.done()]
        
        return future
    
    def submit_batch(self, fn: Callable, items: List[Any]) -> List[Future]:
        """Submit multiple tasks for parallel processing."""
        futures = []
        for item in items:
            if isinstance(item, tuple):
                future = self.submit(fn, *item)
            else:
                future = self.submit(fn, item)
            futures.append(future)
        return futures
    
    def map(self, fn: Callable, items: List[Any], timeout: float = None) -> List[Any]:
        """Map function over items in parallel and return results."""
        if self._executor is None:
            self.start()
        
        return list(self._executor.map(fn, items, timeout=timeout))
    
    def shutdown(self, wait: bool = True):
        """Shutdown the thread pool."""
        if self._executor is not None:
            self._executor.shutdown(wait=wait)
            self._executor = None
            logger.info("Thread pool shut down")
    
    def pending_count(self) -> int:
        """Get number of pending tasks."""
        self._pending_futures = [f for f in self._pending_futures if not f.done()]
        return len(self._pending_futures)
    
    def wait_all(self, timeout: float = None):
        """Wait for all pending tasks to complete."""
        from concurrent.futures import wait
        if self._pending_futures:
            wait(self._pending_futures, timeout=timeout)


# Singleton accessor
def get_pool() -> ThreadPoolManager:
    """Get the global thread pool manager."""
    return ThreadPoolManager()


def get_memory_stats() -> MemoryStats:
    """Get current memory usage for RAM and VRAM."""
    
    # RAM stats
    ram_used = 0
    ram_total = 0
    ram_percent = 0.0
    
    if PSUTIL_AVAILABLE:
        mem = psutil.virtual_memory()
        ram_total = mem.total
        ram_used = mem.used
        ram_percent = mem.percent
    
    # VRAM stats
    vram_used = 0
    vram_total = 0
    vram_percent = 0.0
    device_name = "CPU"
    
    if TORCH_AVAILABLE and torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        vram_total = torch.cuda.get_device_properties(0).total_memory
        vram_used = torch.cuda.memory_allocated(0)
        vram_percent = (vram_used / vram_total) * 100 if vram_total > 0 else 0
    
    return MemoryStats(
        ram_used=ram_used,
        ram_total=ram_total,
        ram_percent=ram_percent,
        vram_used=vram_used,
        vram_total=vram_total,
        vram_percent=vram_percent,
        device_name=device_name,
    )


def format_bytes(size_bytes: int) -> str:
    """Format bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def get_memory_summary() -> str:
    """Get formatted memory usage summary."""
    stats = get_memory_stats()
    
    lines = [
        f"RAM: {format_bytes(stats.ram_used)} / {format_bytes(stats.ram_total)} ({stats.ram_percent:.1f}%)",
    ]
    
    if stats.vram_total > 0:
        lines.append(f"VRAM: {format_bytes(stats.vram_used)} / {format_bytes(stats.vram_total)} ({stats.vram_percent:.1f}%)")
        lines.append(f"GPU: {stats.device_name}")
    
    return "\n".join(lines)


def clear_vram_cache():
    """Clear CUDA memory cache to free VRAM."""
    if TORCH_AVAILABLE and torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        logger.info("Cleared VRAM cache")


def cleanup_after_generation():
    """Run cleanup tasks after generation based on settings."""
    settings = get_settings()
    
    if settings.gc_on_generate:
        gc.collect()
        logger.debug("Garbage collection completed")
    
    if settings.clear_cache_between:
        clear_vram_cache()


def get_optimal_batch_size(vram_gb: float = None) -> int:
    """
    Suggest optimal batch size based on available VRAM.
    
    Args:
        vram_gb: Available VRAM in GB (auto-detect if None)
        
    Returns:
        Suggested batch size
    """
    if vram_gb is None and TORCH_AVAILABLE and torch.cuda.is_available():
        props = torch.cuda.get_device_properties(0)
        vram_gb = props.total_memory / (1024**3)
    
    if vram_gb is None or vram_gb <= 0:
        return 1
    
    if vram_gb >= 16:
        return 4
    elif vram_gb >= 8:
        return 2
    else:
        return 1


# Quantization support
def enable_8bit_loading() -> bool:
    """
    Enable 8-bit model loading to reduce VRAM.
    
    Returns:
        True if 8-bit support is available
    """
    try:
        import bitsandbytes
        logger.info("8-bit quantization available (bitsandbytes)")
        return True
    except ImportError:
        logger.info("8-bit not available. Install: pip install bitsandbytes")
        return False


def load_model_quantized(model_name: str, bits: int = 8):
    """
    Load a HuggingFace model with quantization.
    
    Args:
        model_name: Model name or path
        bits: Quantization bits (4 or 8)
        
    Returns:
        Loaded model or None
    """
    if not TORCH_AVAILABLE:
        return None
    
    try:
        from transformers import AutoModelForCausalLM, BitsAndBytesConfig
        
        if bits == 4:
            config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
            )
        else:
            config = BitsAndBytesConfig(
                load_in_8bit=True,
            )
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=config,
            device_map="auto",
        )
        
        logger.info(f"Loaded {model_name} with {bits}-bit quantization")
        return model
        
    except Exception as e:
        logger.error(f"Failed to load quantized model: {e}")
        return None


def async_save_audio(audio_data, filepath: str, sample_rate: int = 32000):
    """Save audio file asynchronously using thread pool."""
    settings = get_settings()
    
    def _save():
        try:
            import soundfile as sf
            sf.write(filepath, audio_data.T if audio_data.ndim > 1 else audio_data, sample_rate)
            logger.info(f"Async saved: {filepath}")
        except Exception as e:
            logger.error(f"Async save failed: {e}")
    
    if settings.async_save:
        return get_pool().submit(_save)
    else:
        _save()
        return None


def init_performance():
    """Initialize performance settings from environment or defaults."""
    cpu_count = os.cpu_count() or 4
    
    update_settings(
        num_workers=min(4, cpu_count),
        pool_size=4,
        torch_threads=min(4, cpu_count),
    )
    
    # Start thread pool
    get_pool().start()
    
    # Set PyTorch threads
    if TORCH_AVAILABLE:
        torch.set_num_threads(get_settings().torch_threads)
    
    logger.info("Performance subsystem initialized")
