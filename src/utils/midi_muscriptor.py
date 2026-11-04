"""
MuScriptor / NeuralNote Engine Adapter for KraftBeat.

Implements polyphonic, multi-instrument transcription using the official
MuScriptor transcription model (Kyutai + Mirelo, arXiv 2607.08168).

Capability Notes:
- Recovers multiple instrument groups (piano, drums, guitar, bass, etc.)
- Recovers no velocity and no pitch bend dynamics: exports synthesized
  constant velocity (default 100, configurable via 'muscriptor_export_velocity')
- Uses detect_beat_grid_for() with fallback to flagged 120 BPM placeholder grid
- Reports chunk-based progress via ProgressEvent
"""

import logging
from pathlib import Path
from typing import Optional, Callable, Dict, Any, List
import numpy as np

import json
import os
import subprocess
import sys
import threading
import time
from src.models.transcription import TranscriptionNote, TranscriptionResult
from src.utils.config import get_config
from src.utils.model_manager import ModelManager

logger = logging.getLogger(__name__)


class MuscriptorWorkerProcess:
    """
    Manages an isolated child process running src/utils/muscriptor_worker.py.
    Coordinates GPU leasing and communicates via newline-delimited JSON.
    """

    def __init__(self, python_path: Optional[str] = None):
        self.python_path = python_path or get_config("muscriptor_python") or sys.executable
        self._proc: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()

    def start(self) -> None:
        worker_script = Path(__file__).parent / "muscriptor_worker.py"
        env = os.environ.copy()
        try:
            from src.utils.credentials import get_credential
            token = get_credential("huggingface_token")
            if token:
                env["HF_TOKEN"] = token
        except Exception:
            pass

        self._proc = subprocess.Popen(
            [self.python_path, str(worker_script)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env
        )
        ModelManager.register_lease_process(self._proc)

        # Handshake: wait for ready event
        ready_line = self._proc.stdout.readline()
        if not ready_line:
            code = self._proc.poll()
            err = self._proc.stderr.read() if self._proc.stderr else ""
            raise RuntimeError(f"MuScriptor worker failed to start (exit code {code}): {err}")
        try:
            ev = json.loads(ready_line.strip())
            if ev.get("event") != "ready":
                logger.warning(f"Unexpected worker handshake event: {ev}")
        except Exception as e:
            logger.warning(f"Could not parse worker ready line: {e}")

    def send_cmd(self, cmd_dict: Dict[str, Any]) -> None:
        if not self._proc or self._proc.poll() is not None:
            raise RuntimeError("Worker process is not running.")
        line = json.dumps(cmd_dict) + "\n"
        self._proc.stdin.write(line)
        self._proc.stdin.flush()

    def transcribe(
        self,
        audio_path: str,
        model_size: str = "small",
        velocity: int = 100,
        progress_callback: Optional[Callable[[float, str], None]] = None,
    ) -> Dict[str, Any]:
        with self._lock:
            if not self._proc or self._proc.poll() is not None:
                self.start()

            job_id = f"job_musc_{int(time.time() * 1000)}"
            self.send_cmd({"cmd": "load", "model_size": model_size})
            self.send_cmd({
                "cmd": "transcribe",
                "job_id": job_id,
                "audio_path": str(Path(audio_path).resolve()),
                "velocity": velocity,
            })

            while True:
                line = self._proc.stdout.readline()
                if not line:
                    code = self._proc.poll()
                    err = self._proc.stderr.read() if self._proc.stderr else ""
                    raise RuntimeError(f"MuScriptor worker exited unexpectedly (code {code}): {err}")
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except Exception:
                    continue

                ev_type = event.get("event")
                if ev_type == "progress":
                    if progress_callback:
                        pct = float(event.get("progress", 0.0))
                        c = event.get("chunk", 0)
                        t = event.get("total_chunks", 1)
                        progress_callback(pct, f"Transcribing ({c}/{t} chunks)...")
                elif ev_type == "result":
                    return event.get("result", {})
                elif ev_type == "cancelled":
                    raise InterruptedError("Transcription cancelled.")
                elif ev_type == "error":
                    raise RuntimeError(f"MuScriptor worker error [{event.get('type')}]: {event.get('message')}")

    def cancel(self, job_id: Optional[str] = None) -> None:
        if self._proc and self._proc.poll() is None:
            try:
                self.send_cmd({"cmd": "cancel", "job_id": job_id})
            except Exception as e:
                logger.warning(f"Failed to send cancel to worker: {e}")

    def shutdown(self) -> None:
        if self._proc:
            try:
                self.send_cmd({"cmd": "shutdown"})
                self._proc.wait(timeout=2.0)
            except Exception:
                if self._proc.poll() is None:
                    self._proc.terminate()
                    try:
                        self._proc.wait(timeout=2.0)
                    except Exception:
                        self._proc.kill()
            self._proc = None


def transcribe_muscriptor(
    audio_path: str,
    output_path: Optional[str] = None,
    model_size: str = "small",
    progress_callback: Optional[Callable[[float, str], None]] = None,
    device: Optional[str] = None,
    prefer_worker: bool = True,
) -> Optional[TranscriptionResult]:
    """
    Transcribe audio file using the MuScriptor engine.
    
    Args:
        audio_path: Path to source audio file
        output_path: Optional destination path for .mid file
        model_size: Model size ('small' | 'medium' | 'large')
        progress_callback: Optional callback(fraction 0.0-1.0, status_text)
        device: Optional torch device string
        prefer_worker: Whether to run in isolated worker process (default True)
        
    Returns:
        TranscriptionResult object if successful, None on error.
    """
    if not Path(audio_path).exists():
        logger.error(f"Audio file does not exist: {audio_path}")
        return None

    # Check if in-process muscriptor is available and requested
    in_process_available = False
    if not prefer_worker:
        try:
            from muscriptor.transcription_model import TranscriptionModel
            from muscriptor.utils.midi import detect_beat_grid_for
            in_process_available = True
        except ImportError:
            in_process_available = False

    export_velocity = int(get_config("muscriptor_export_velocity", 100))

    if prefer_worker or not in_process_available:
        # Run via isolated child process
        lease_granted = ModelManager.acquire_gpu(owner="muscriptor", kind="external_process")
        if not lease_granted:
            logger.error("Could not acquire GPU lease for MuScriptor worker.")
            return None

        worker = MuscriptorWorkerProcess()
        try:
            logger.info(f"Running MuScriptor transcription via isolated worker ({model_size})...")
            if progress_callback:
                progress_callback(0.05, f"Spawning MuScriptor {model_size} worker...")

            res_dict = worker.transcribe(
                audio_path=audio_path,
                model_size=model_size,
                velocity=export_velocity,
                progress_callback=progress_callback,
            )

            notes_data = res_dict.get("notes", [])
            notes = [
                TranscriptionNote(
                    onset_sec=float(n.get("start", 0.0)),
                    offset_sec=float(n.get("end", 0.0)),
                    pitch=int(n.get("pitch", 60)),
                    instrument=str(n.get("instrument", "acoustic_grand_piano")),
                    velocity=None,
                    pitch_bend=None,
                )
                for n in notes_data
            ]

            duration = max((n.offset_sec for n in notes), default=0.0)
            try:
                import soundfile as sf
                info = sf.info(audio_path)
                duration = info.duration
            except Exception:
                pass

            result = TranscriptionResult(
                notes=notes,
                tempo=float(res_dict.get("bpm", 120.0)),
                time_signature=res_dict.get("time_signature"),
                is_placeholder_grid=bool(res_dict.get("is_placeholder_grid", False)),
                duration=duration,
                source_audio_path=audio_path,
                engine_id="muscriptor",
                model_size=model_size,
                has_velocity=False,
                has_pitch_bend=False,
            )

            if output_path:
                result.save_midi(output_path)
                logger.info(f"Saved MuScriptor MIDI to: {output_path}")

            if progress_callback:
                progress_callback(1.0, "Transcription complete")

            return result

        except Exception as e:
            logger.error(f"MuScriptor worker transcription failed: {e}")
            return None
        finally:
            worker.shutdown()
            ModelManager.release_gpu(owner="muscriptor")

    # In-process path
    try:
        from muscriptor.transcription_model import TranscriptionModel
        from muscriptor.utils.midi import detect_beat_grid_for
        logger.info(f"Loading MuScriptor ({model_size}) model in-process...")
        if progress_callback:
            progress_callback(0.05, f"Loading MuScriptor {model_size} model...")

        model = TranscriptionModel.load_model(model_size, device=device)

        # Detect beat grid
        if progress_callback:
            progress_callback(0.15, "Detecting tempo and beat grid...")

        is_placeholder = False
        try:
            beat_grid = detect_beat_grid_for(audio_path, mode="best-effort")
            tempo = getattr(beat_grid, "bpm", 120.0)
            time_signature = getattr(beat_grid, "time_signature", None)
        except Exception as e:
            logger.warning(f"Beat grid detection failed ({e}), using 120 BPM placeholder")
            beat_grid = None
            tempo = 120.0
            time_signature = None
            is_placeholder = True

        # Run transcription generator
        logger.info(f"Transcribing {audio_path} with MuScriptor...")
        events = []
        notes: List[TranscriptionNote] = []
        active_notes: Dict[int, float] = {}  # pitch -> onset_sec

        gen = model.transcribe(audio_path)
        for event in gen:
            events.append(event)
            event_type = event.__class__.__name__

            if event_type == "ProgressEvent":
                completed = getattr(event, "completed_chunks", 0)
                total = getattr(event, "total_chunks", 1)
                fraction = 0.2 + 0.7 * (completed / max(total, 1))
                if progress_callback:
                    progress_callback(fraction, f"Transcribing ({completed}/{total} chunks)...")

            elif event_type == "NoteStartEvent":
                pitch = getattr(event, "pitch", 60)
                time_sec = getattr(event, "time", 0.0)
                active_notes[pitch] = time_sec

            elif event_type == "NoteEndEvent":
                pitch = getattr(event, "pitch", 60)
                end_sec = getattr(event, "time", 0.0)
                inst = getattr(event, "instrument", "acoustic_grand_piano")
                onset_sec = active_notes.pop(pitch, 0.0)
                notes.append(
                    TranscriptionNote(
                        onset_sec=onset_sec,
                        offset_sec=end_sec,
                        pitch=pitch,
                        instrument=inst,
                        velocity=None,  # MuScriptor does not recover velocity
                        pitch_bend=None,  # MuScriptor does not recover pitch bend
                    )
                )

        if progress_callback:
            progress_callback(0.95, "Serializing MIDI events...")

        # Export velocity configuration
        export_velocity = int(get_config("muscriptor_export_velocity", 100))

        # Reconstruct byte-identical MIDI bytes using official helper
        midi_bytes = model.events_to_midi_bytes(
            events,
            beat_grid=beat_grid,
            velocity=export_velocity
        )

        # Duration
        import soundfile as sf
        try:
            info = sf.info(audio_path)
            duration = info.duration
        except Exception:
            duration = max((n.offset_sec for n in notes), default=0.0)

        result = TranscriptionResult(
            notes=notes,
            tempo=tempo,
            time_signature=time_signature,
            is_placeholder_grid=is_placeholder,
            duration=duration,
            source_audio_path=audio_path,
            engine_id="muscriptor",
            model_size=model_size,
            has_velocity=False,
            has_pitch_bend=False,
            midi_bytes=midi_bytes,
        )

        if output_path:
            result.save_midi(output_path)
            logger.info(f"Saved MuScriptor MIDI to: {output_path}")

        if progress_callback:
            progress_callback(1.0, "Transcription complete")

        return result

    except Exception as e:
        logger.error(f"MuScriptor transcription error: {e}")
        return None
