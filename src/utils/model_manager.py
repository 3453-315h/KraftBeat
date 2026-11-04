"""
Model Manager for Kraftbeat.

Ensures that only one heavy AI model is loaded in VRAM at a time.
Provides a process-level GPU lease system that supports both in-process loaders
and external child processes (e.g. Aoide/YuE2 workers, transcription workers, ComfyUI).
"""

import logging
import gc
import time
import subprocess
from dataclasses import dataclass
from typing import Optional, Any, Callable

logger = logging.getLogger(__name__)


@dataclass
class GpuLease:
    owner_id: str
    kind: str  # 'in_process' | 'external_process'
    loader: Optional[Any] = None
    proc: Optional[subprocess.Popen] = None
    unload_fn: Optional[Callable[[], None]] = None


class ModelManager:
    """
    Singleton manager to enforce 'Single Active Heavy Model / GPU Lease' policy.
    
    Usage:
        ModelManager.instance().prepare_load(new_loader)
        or
        ModelManager.instance().acquire_gpu(owner_id="aoide_worker", kind="external_process", proc=subproc)
    """
    
    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ModelManager()
        return cls._instance
        
    def __init__(self):
        self.active_loader: Optional[Any] = None
        self.active_model_name: str = ""
        self.current_lease: Optional[GpuLease] = None

    def acquire_gpu(
        self,
        owner_id: str,
        kind: str = "in_process",
        loader: Optional[Any] = None,
        proc: Optional[subprocess.Popen] = None,
        unload_fn: Optional[Callable[[], None]] = None,
        timeout_seconds: float = 10.0,
    ) -> bool:
        """
        Acquire exclusive GPU/VRAM lease for an in-process loader or external process.
        If another owner holds the lease, requests graceful unload, waits, and if necessary
        terminates/kills child processes to confirm complete exit before granting the lease.
        
        Returns:
            True if lease acquired, False if previous owner refused/failed to release.
        """
        # Re-entrant check for same owner
        if self.current_lease is not None and self.current_lease.owner_id == owner_id:
            # Update proc/loader if refreshed
            if loader is not None:
                self.current_lease.loader = loader
            if proc is not None:
                self.current_lease.proc = proc
            return True

        # If a different lease is active, revoke it cleanly
        if self.current_lease is not None:
            prev = self.current_lease
            logger.info(f"Revoking GPU lease from previous owner: {prev.owner_id} ({prev.kind})")
            
            # 1. In-process unload
            if prev.unload_fn is not None:
                try:
                    prev.unload_fn()
                except Exception as e:
                    logger.error(f"Error calling unload_fn for {prev.owner_id}: {e}")
            elif prev.loader is not None and hasattr(prev.loader, 'unload'):
                try:
                    prev.loader.unload()
                except Exception as e:
                    logger.error(f"Error unloading previous loader {prev.owner_id}: {e}")

            # 2. External child process termination & verified exit
            if prev.proc is not None:
                if prev.proc.poll() is None:
                    # Give it a grace period to exit gracefully
                    grace = min(timeout_seconds * 0.5, 3.0)
                    start_wait = time.time()
                    while prev.proc.poll() is None and (time.time() - start_wait) < grace:
                        time.sleep(0.1)

                    if prev.proc.poll() is None:
                        logger.warning(f"Process for {prev.owner_id} did not exit gracefully; terminating...")
                        try:
                            prev.proc.terminate()
                        except OSError:
                            pass
                        
                        term_wait = time.time()
                        while prev.proc.poll() is None and (time.time() - term_wait) < 2.0:
                            time.sleep(0.1)

                    if prev.proc.poll() is None:
                        logger.error(f"Process for {prev.owner_id} failed to terminate; killing...")
                        try:
                            prev.proc.kill()
                            prev.proc.wait(timeout=2.0)
                        except (OSError, subprocess.TimeoutExpired) as e:
                            logger.critical(f"Failed to kill process {prev.proc.pid}: {e}")
                            return False

            self.current_lease = None
            self.active_loader = None
            self.active_model_name = ""
            self.force_cleanup()

        # Grant new lease
        self.current_lease = GpuLease(
            owner_id=owner_id,
            kind=kind,
            loader=loader,
            proc=proc,
            unload_fn=unload_fn
        )
        if kind == "in_process" and loader is not None:
            self.active_loader = loader
            self.active_model_name = owner_id
        logger.info(f"GPU lease granted to {owner_id} ({kind})")
        return True

    def release_gpu(self, owner_id: str) -> None:
        """Release the GPU lease held by owner_id."""
        if self.current_lease is not None and self.current_lease.owner_id == owner_id:
            logger.info(f"Releasing GPU lease for {owner_id}")
            self.current_lease = None
            self.active_loader = None
            self.active_model_name = ""
            self.force_cleanup()

    def prepare_load(self, loader: Any, model_name: str = "") -> None:
        """
        Backward-compatible helper: calls acquire_gpu for an in-process loader.
        """
        owner = model_name or loader.__class__.__name__
        unload_fn = getattr(loader, 'unload', None)
        self.acquire_gpu(owner_id=owner, kind="in_process", loader=loader, unload_fn=unload_fn)
        
    def force_cleanup(self):
        """Force Python GC and CUDA cache cleanup."""
        gc.collect()
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
        except Exception as e:
            logger.debug(f"Torch CUDA cleanup skipped/failed: {e}")
        logger.info("VRAM cleanup performed.")

    def get_active_model_name(self) -> str:
        if self.current_lease:
            return self.current_lease.owner_id
        return self.active_model_name

