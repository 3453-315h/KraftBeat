"""
Kraftbeat REST API Server

A lightweight FastAPI server embedded inside Kraftbeat for headless 
operation and DAW integration. Runs in a background thread.

Endpoints:
    GET  /             → API info / health check
    GET  /models       → List available models
    POST /generate     → Start a generation job
    GET  /status       → Poll current generation status
    POST /stop         → Stop current generation
    GET  /outputs      → List completed outputs
"""

import asyncio
import logging
import os
import time
import uuid
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# --- Shared State ---
# This module-level state is how the API communicates with the PyQt backend.
# The MainWindow will inject references into this dict at startup.
import threading

_state_lock = threading.Lock()
_jobs: Dict[str, Dict[str, Any]] = {}
_state: Dict[str, Any] = {
    "loader": None,          # MusicGenLoader instance (injected by MainWindow)
    "is_generating": False,
    "current_job_id": None,
    "current_status": "idle",
    "current_progress": 0,
    "last_output_path": None,
    "start_time": None,
    "stop_requested": False,
}


def get_state() -> Dict[str, Any]:
    with _state_lock:
        return _state.copy()


def set_loader(loader):
    """Called by MainWindow to inject the active model loader into the API state."""
    with _state_lock:
        _state["loader"] = loader
    logger.info("API: Loader reference injected.")


def create_app():
    """Create and return the FastAPI application instance."""
    try:
        from fastapi import FastAPI, HTTPException, BackgroundTasks
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel
    except ImportError:
        logger.error("FastAPI not installed. Run: pip install fastapi uvicorn[standard]")
        return None

    try:
        from src import __version__
        api_version = __version__
    except ImportError:
        api_version = "1.0.0"

    app = FastAPI(
        title="Kraftbeat API",
        description="Headless REST API for AI music generation. For DAW and script integration.",
        version=api_version,
    )

    from src.utils.config import get_config

    cors_origins = get_config("api_cors_origins", [
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:8765",
        "http://127.0.0.1:8765",
    ])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Request Models ---

    class GenerateRequest(BaseModel):
        prompt: str
        duration: int = 30
        model: Optional[str] = None
        temperature: float = 1.0
        top_k: int = 250
        top_p: float = 0.0
        cfg_coef: float = 3.0
        seed: Optional[int] = None

    @app.get("/", tags=["Health"])
    def root():
        host = get_config("api_host", "localhost")
        port = get_config("api_port", 8765)
        return {
            "name": "Kraftbeat API",
            "version": "1.0.0",
            "status": "running",
            "docs": f"http://{host}:{port}/docs",
        }

    @app.get("/models", tags=["Models"])
    def list_models():
        """List all available MusicGen models and their status."""
        try:
            from src.models.musicgen import MUSICGEN_MODELS
            from src.utils.cache import get_cached_models
            cached = [m["name"] for m in get_cached_models()]
            return {
                "models": [
                    {
                        "name": name,
                        "params": info.get("params"),
                        "vram_gb": info.get("vram_gb"),
                        "stereo": info.get("stereo", False),
                        "melody": info.get("melody", False),
                        "downloaded": any(info.get("id", "") in c for c in cached),
                    }
                    for name, info in MUSICGEN_MODELS.items()
                ]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/generate", tags=["Generation"])
    def start_generation(req: GenerateRequest, background_tasks: BackgroundTasks):
        """Start a music generation job. Returns a job_id to poll /status with."""
        with _state_lock:
            if _state["is_generating"]:
                raise HTTPException(
                    status_code=409,
                    detail="A generation is already in progress. Poll /status or POST /stop first."
                )

            loader = _state.get("loader")
            if not loader or not getattr(loader, "model", None):
                raise HTTPException(
                    status_code=503,
                    detail="No model is loaded. Please load a model via the Kraftbeat UI first."
                )

            job_id = str(uuid.uuid4())[:8]
            _state["current_job_id"] = job_id
            _state["is_generating"] = True
            _state["current_status"] = "generating"
            _state["current_progress"] = 0
            _state["last_output_path"] = None
            _state["start_time"] = time.time()
            _state["stop_requested"] = False

            _jobs[job_id] = {
                "job_id": job_id,
                "is_generating": True,
                "status": "generating",
                "progress": 0,
                "elapsed_seconds": 0.0,
                "output_path": None,
                "start_time": _state["start_time"],
            }

        background_tasks.add_task(_run_generation, req, job_id)

        return {
            "job_id": job_id,
            "status": "started",
            "message": f"Generation started. Poll GET /status?job_id={job_id} for updates.",
        }

    @app.get("/status", tags=["Generation"])
    def get_status(job_id: Optional[str] = None):
        """Poll the status of the current or specified generation job."""
        with _state_lock:
            if job_id is not None:
                if job_id == _state.get("current_job_id"):
                    elapsed = round(time.time() - _state["start_time"], 1) if _state.get("start_time") else 0.0
                    return {
                        "job_id": _state["current_job_id"],
                        "is_generating": _state["is_generating"],
                        "status": _state["current_status"],
                        "progress": _state["current_progress"],
                        "elapsed_seconds": elapsed,
                        "output_path": _state["last_output_path"],
                    }
                if job_id in _jobs:
                    job_info = dict(_jobs[job_id])
                    job_info.pop("start_time", None)
                    return job_info
                raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

            # Fallback to current job status if job_id is omitted
            elapsed = round(time.time() - _state["start_time"], 1) if _state.get("start_time") else 0.0
            return {
                "job_id": _state["current_job_id"],
                "is_generating": _state["is_generating"],
                "status": _state["current_status"],
                "progress": _state["current_progress"],
                "elapsed_seconds": elapsed,
                "output_path": _state["last_output_path"],
            }

    @app.post("/stop", tags=["Generation"])
    def stop_generation():
        """Request cancellation of the current generation job."""
        with _state_lock:
            if not _state["is_generating"]:
                return {"message": "No generation in progress."}
            _state["stop_requested"] = True
            _state["current_status"] = "stopping"
            loader = _state.get("loader")
            if loader and hasattr(loader, "stop"):
                loader.stop()
            curr_id = _state.get("current_job_id")
            if curr_id and curr_id in _jobs:
                _jobs[curr_id]["status"] = "stopping"
        return {"message": "Stop requested. Generation will halt at the next checkpoint."}

    @app.get("/outputs", tags=["Outputs"])
    def list_outputs():
        """List all WAV files in the outputs/ directory."""
        outputs_dir = os.path.join(os.getcwd(), "outputs")
        if not os.path.exists(outputs_dir):
            return {"outputs": []}

        files = []
        for f in sorted(os.listdir(outputs_dir), reverse=True):
            if f.endswith(".wav") or f.endswith(".mp3") or f.endswith(".flac"):
                path = os.path.join(outputs_dir, f)
                files.append({
                    "filename": f,
                    "path": path,
                    "size_kb": round(os.path.getsize(path) / 1024, 1),
                    "modified": os.path.getmtime(path),
                })
        return {"outputs": files[:50]}  # Return last 50

    return app


def _run_generation(req, job_id: str):
    """Background task that actually runs the generation (runs in Uvicorn thread pool)."""
    import numpy as np
    from datetime import datetime

    def _sync_job(status: Optional[str] = None, progress: Optional[int] = None, output_path: Optional[str] = None, is_generating: Optional[bool] = None):
        with _state_lock:
            if status is not None:
                _state["current_status"] = status
            if progress is not None:
                _state["current_progress"] = progress
            if output_path is not None:
                _state["last_output_path"] = output_path
            if is_generating is not None:
                _state["is_generating"] = is_generating
            
            if job_id in _jobs:
                st = _jobs[job_id].get("start_time", time.time())
                _jobs[job_id]["elapsed_seconds"] = round(time.time() - st, 1)
                if status is not None:
                    _jobs[job_id]["status"] = status
                if progress is not None:
                    _jobs[job_id]["progress"] = progress
                if output_path is not None:
                    _jobs[job_id]["output_path"] = output_path
                if is_generating is not None:
                    _jobs[job_id]["is_generating"] = is_generating

    try:
        with _state_lock:
            loader = _state.get("loader")
            if not loader or not getattr(loader, "model", None):
                _sync_job(status="error", is_generating=False)
                return
            if hasattr(loader, "reset_stop"):
                loader.reset_stop()
            elif hasattr(loader, "_stop_requested"):
                loader._stop_requested = False

        def progress_cb(current, total):
            with _state_lock:
                if _state.get("stop_requested"):
                    return False
                pct = int(min(90, max(10, (current / max(1, total)) * 80 + 10)))
                _sync_job(progress=pct)
            return True

        params = {
            "prompt": req.prompt,
            "duration": req.duration,
            "temperature": req.temperature,
            "top_k": req.top_k,
            "top_p": req.top_p,
            "cfg_coef": req.cfg_coef,
            "progress_callback": progress_cb,
        }

        logger.info(f"[API] Starting generation job {job_id}: '{req.prompt[:50]}...'")
        _sync_job(progress=10)

        audio = loader.generate(**params)

        with _state_lock:
            if _state.get("stop_requested"):
                _sync_job(status="stopped", is_generating=False)
                return

        if audio is None:
            _sync_job(status="error", is_generating=False)
            return

        # Save output
        outputs_dir = os.path.join(os.getcwd(), "outputs")
        os.makedirs(outputs_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = req.prompt[:25].replace(" ", "_").replace(",", "")
        filename = f"{timestamp}_api_{job_id}_{slug}.wav"
        filepath = os.path.join(outputs_dir, filename)

        try:
            import soundfile as sf
            if audio.ndim == 2 and audio.shape[0] <= 2:
                audio_to_save = audio.T
            else:
                audio_to_save = audio
            sr = getattr(loader, "sample_rate", 32000)
            sf.write(filepath, audio_to_save, sr)
            logger.info(f"[API] Job {job_id} complete → {filepath}")
            _sync_job(status="complete", progress=100, output_path=filepath, is_generating=False)
        except Exception as e:
            logger.error(f"[API] Failed to save output: {e}")
            _sync_job(status="error", is_generating=False)
            return

    except Exception as e:
        logger.error(f"[API] Generation job {job_id} failed: {e}")
        import traceback
        traceback.print_exc()
        _sync_job(status="error", is_generating=False)
    finally:
        with _state_lock:
            _state["is_generating"] = False
            if job_id in _jobs:
                _jobs[job_id]["is_generating"] = False
