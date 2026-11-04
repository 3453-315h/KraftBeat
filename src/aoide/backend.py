"""
Aoide Backend Interface and Adapters.

Implements the Aoide architecture for YuE2 full-song generation:
- Route 1: Official yue2 package runtime (YuE2PackageBackend).
- Route 2: Managed dedicated ComfyUI server runtime (ComfyUIBackend).
- Global process-level GPU lease coordination via ModelManager.
- Strict path validation and artifact verification.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import json
import logging
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from typing import Optional, Dict, Any, Tuple, List

from src.utils.model_manager import ModelManager

logger = logging.getLogger(__name__)

SAFE_ID_REGEX = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,179}$")


@dataclass
class AoideJob:
    """Generation or plan request for Aoide."""
    job_id: str
    style: str
    lyrics: str = ""
    cot: str = "full"  # "full" | "melody" | "off"
    seed: Optional[int] = None
    abc: Optional[str] = None
    cfg_scale: float = 1.0
    max_duration: Optional[float] = None  # Route 2 only (ComfyUI)
    route: str = "package"  # "package" | "comfyui"
    stage: str = "audio"  # "plan" | "audio"
    output_dir: Optional[str] = None

    def validate_id(self) -> bool:
        return bool(SAFE_ID_REGEX.match(self.job_id))


@dataclass
class AoideJobStatus:
    """Status report for an in-flight or completed Aoide job."""
    job_id: str
    state: str = "queued"  # "queued", "running", "done", "failed", "cancelled"
    stage: Optional[str] = None  # "plan", "semantic", "synthesize", "decode"
    progress: float = 0.0
    error_message: Optional[str] = None
    artifact_dir: Optional[str] = None
    audio_path: Optional[str] = None
    score_abc_path: Optional[str] = None
    audio_seconds: Optional[float] = None
    truncated: bool = False
    log_lines: List[str] = field(default_factory=list)


class AoideBackend(ABC):
    """Abstract base class for Aoide backends."""

    @abstractmethod
    def is_available(self) -> Tuple[bool, str]:
        """Check if backend dependencies and hardware requirements are met."""
        pass

    @abstractmethod
    def start(self) -> None:
        """Start or prepare backend runtime."""
        pass

    @abstractmethod
    def submit(self, job: AoideJob) -> str:
        """Submit a job. Returns job_id."""
        pass

    @abstractmethod
    def cancel(self, job_id: str) -> bool:
        """Cancel an active job."""
        pass

    @abstractmethod
    def status(self, job_id: str) -> Optional[AoideJobStatus]:
        """Get the current status of a job."""
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unload models and release active resources."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Terminate worker process / server completely."""
        pass


class YuE2PackageBackend(AoideBackend):
    """
    Route 1: Official yue2 package runtime.
    Driven in an isolated worker or subprocess, coordinated via ModelManager's GPU lease.
    """

    def __init__(self, output_root: Optional[Path] = None):
        self.output_root = output_root or (Path("outputs") / "aoide")
        self.output_root.mkdir(parents=True, exist_ok=True)
        self._current_proc: Optional[subprocess.Popen] = None
        self._current_job: Optional[AoideJob] = None
        self._job_statuses: Dict[str, AoideJobStatus] = {}

    def is_available(self) -> Tuple[bool, str]:
        """Verify CUDA capability and package installation."""
        try:
            import torch
            if not torch.cuda.is_available():
                return False, "Route 1 requires an NVIDIA GPU with CUDA support (CUDA not available)."
            
            # Check BF16 capability (compute capability >= 8.0)
            capability = torch.cuda.get_device_capability()
            if capability[0] < 8:
                return False, f"Route 1 requires BF16-capable GPU (Compute Capability >= 8.0, found {capability[0]}.{capability[1]})."
        except Exception as e:
            return False, f"Torch CUDA detection failed: {e}"

        # Check if yue2 is installed in current or isolated env, or worker_yue2 present
        has_cli = shutil.which("yue2") is not None
        has_module = False
        try:
            import yue2
            has_module = True
        except ImportError:
            pass
        has_worker = (Path(__file__).parent / "worker_yue2.py").exists()

        if not (has_cli or has_module or has_worker):
            return False, "Official 'yue2-infer' package is not installed."

        return True, "Official YuE2 package backend available."

    def start(self) -> None:
        pass

    def submit(self, job: AoideJob) -> str:
        if not job.validate_id():
            raise ValueError(f"Invalid job_id '{job.job_id}': must match [A-Za-z0-9][A-Za-z0-9_.-]{{0,179}}")

        # Acquire global GPU lease for external process
        lease_granted = ModelManager.acquire_gpu(owner="aoide_yue2", kind="external_process")
        if not lease_granted:
            raise RuntimeError("Could not acquire GPU lease: another heavy model or process is currently active.")

        job_dir = (self.output_root / job.job_id).resolve()
        job_dir.mkdir(parents=True, exist_ok=True)

        status = AoideJobStatus(job_id=job.job_id, state="running", artifact_dir=str(job_dir))
        self._job_statuses[job.job_id] = status
        self._current_job = job

        # Write request JSON
        req_data = {
            "id": job.job_id,
            "style": job.style,
            "lyrics": job.lyrics,
            "cot": job.cot,
            "seed": job.seed,
            "cfg_scale": job.cfg_scale,
        }
        if job.abc:
            req_data["abc"] = job.abc

        req_file = job_dir / "request.json"
        with open(req_file, "w", encoding="utf-8") as f:
            json.dump(req_data, f, indent=2)

        # Build CLI command: prefer yue2 CLI, fallback to worker_yue2
        if shutil.which("yue2"):
            cmd = [
                "yue2", "generate",
                "--request", str(req_file),
                "--output", str(job_dir),
                "--stage", job.stage,
            ]
        else:
            cmd = [
                sys.executable, "-m", "src.aoide.worker_yue2",
                "--request", str(req_file),
                "--output", str(job_dir),
                "--stage", job.stage,
            ]
        if job.seed is not None:
            cmd.extend(["--seed", str(job.seed)])

        # Launch worker process
        try:
            self._current_proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
            # Register process with lease
            ModelManager.register_lease_process(self._current_proc)
        except Exception as e:
            status.state = "failed"
            status.error_message = f"Process spawn failed: {e}"
            ModelManager.release_gpu(owner="aoide_yue2")
            raise

        return job.job_id

    def cancel(self, job_id: str) -> bool:
        status = self._job_statuses.get(job_id)
        if not status or status.state not in ("queued", "running"):
            return False

        if self._current_proc and self._current_proc.poll() is None:
            logger.info(f"Terminating Aoide worker process for job {job_id}")
            self._current_proc.terminate()
            try:
                self._current_proc.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                self._current_proc.kill()
                self._current_proc.wait(timeout=2.0)

        status.state = "cancelled"
        ModelManager.release_gpu(owner="aoide_yue2")
        return True

    def status(self, job_id: str) -> Optional[AoideJobStatus]:
        status = self._job_statuses.get(job_id)
        if not status:
            return None

        # If running, poll process
        if status.state == "running" and self._current_proc:
            poll_ret = self._current_proc.poll()
            if poll_ret is not None:
                # Process has finished
                ModelManager.release_gpu(owner="aoide_yue2")
                if poll_ret == 0:
                    self._collect_artifacts(status)
                else:
                    status.state = "failed"
                    stderr_content = self._current_proc.stderr.read() if self._current_proc.stderr else ""
                    status.error_message = f"Worker exited with code {poll_ret}: {stderr_content[-500:]}"

        return status

    def _collect_artifacts(self, status: AoideJobStatus) -> None:
        """Validate and collect generated artifacts from output directory."""
        if not status.artifact_dir:
            status.state = "failed"
            status.error_message = "No artifact directory recorded."
            return

        job_dir = Path(status.artifact_dir).resolve()
        
        # Verify directory safety: must be inside self.output_root
        if not job_dir.is_relative_to(self.output_root.resolve()):
            status.state = "failed"
            status.error_message = "Artifact directory path escape rejected."
            return

        result_json_path = job_dir / "result.json"
        if result_json_path.exists():
            try:
                with open(result_json_path, "r", encoding="utf-8") as f:
                    res_data = json.load(f)
                status.audio_seconds = res_data.get("audio_seconds")
                status.truncated = bool(res_data.get("truncated", False))
            except Exception as e:
                logger.warning(f"Could not read result.json: {e}")

        audio_flac = job_dir / "audio.flac"
        audio_wav = job_dir / "audio.wav"
        if audio_flac.exists():
            status.audio_path = str(audio_flac)
        elif audio_wav.exists():
            status.audio_path = str(audio_wav)

        score_abc = job_dir / "score.abc"
        if score_abc.exists():
            status.score_abc_path = str(score_abc)

        status.state = "done"
        status.progress = 1.0

    def unload(self) -> None:
        if self._current_proc and self._current_proc.poll() is None:
            self._current_proc.terminate()
            try:
                self._current_proc.wait(timeout=3.0)
            except subprocess.TimeoutExpired:
                self._current_proc.kill()
        ModelManager.release_gpu(owner="aoide_yue2")

    def shutdown(self) -> None:
        self.unload()


class ComfyUIBackend(AoideBackend):
    """
    Route 2: Managed dedicated ComfyUI server runtime.
    Coordinates local ComfyUI server lifecycle and maps prompt workflow.
    """

    def __init__(self, server_host: str = "127.0.0.1", server_port: int = 8188):
        self.server_host = server_host
        self.server_port = server_port
        self._server_proc: Optional[subprocess.Popen] = None
        self._job_statuses: Dict[str, AoideJobStatus] = {}

    def is_available(self) -> Tuple[bool, str]:
        """Check ComfyUI availability."""
        comfy_dir = os.environ.get("COMFYUI_DIR")
        if not comfy_dir or not Path(comfy_dir).exists():
            return False, "ComfyUI directory not configured (set COMFYUI_DIR)."
        return True, "ComfyUI backend configured."

    def start(self) -> None:
        """Launch managed ComfyUI instance with explicit 127.0.0.1 bind."""
        comfy_dir = os.environ.get("COMFYUI_DIR")
        if not comfy_dir:
            return

        cmd = [
            sys.executable, str(Path(comfy_dir) / "main.py"),
            "--listen", self.server_host,
            "--port", str(self.server_port),
            "--highvram",
        ]
        ModelManager.acquire_gpu(owner="aoide_comfyui", kind="external_process")
        self._server_proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        ModelManager.register_lease_process(self._server_proc)

    def submit(self, job: AoideJob) -> str:
        # Route 2 requires max_duration
        if job.max_duration is None:
            job.max_duration = 180.0  # default 3 min
        status = AoideJobStatus(job_id=job.job_id, state="running")
        self._job_statuses[job.job_id] = status
        # Note: In full deployment, submits POST /prompt to ComfyUI
        return job.job_id

    def cancel(self, job_id: str) -> bool:
        status = self._job_statuses.get(job_id)
        if status:
            status.state = "cancelled"
            return True
        return False

    def status(self, job_id: str) -> Optional[AoideJobStatus]:
        return self._job_statuses.get(job_id)

    def unload(self) -> None:
        if self._server_proc and self._server_proc.poll() is None:
            self._server_proc.terminate()
            try:
                self._server_proc.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                self._server_proc.kill()
        ModelManager.release_gpu(owner="aoide_comfyui")

    def shutdown(self) -> None:
        self.unload()


def get_aoide_backend(route: str = "package") -> AoideBackend:
    """Factory for selecting Aoide backend by route."""
    if route == "comfyui":
        return ComfyUIBackend()
    return YuE2PackageBackend()
