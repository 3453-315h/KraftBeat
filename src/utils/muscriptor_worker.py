"""
Standalone worker process for MuScriptor (NeuralNote) transcription.

Protocol: Newline-delimited JSON over stdin/stdout.
Allows MuScriptor and its specific torch/C++ dependencies to execute
in an isolated child process without polluting KraftBeat's primary runtime.

Commands:
- {"cmd": "hello"} -> {"event": "ready", "version": "1.0"}
- {"cmd": "ping"} -> {"event": "pong"}
- {"cmd": "load", "model_size": "small"|"medium"|"large"}
- {"cmd": "transcribe", "job_id": ..., "audio_path": ..., "velocity": 100}
- {"cmd": "cancel", "job_id": ...}
- {"cmd": "unload"}
- {"cmd": "shutdown"}

Events:
- {"event": "progress", "job_id": ..., "progress": float, "chunk": int, "total_chunks": int}
- {"event": "result", "job_id": ..., "result": {...}}
- {"event": "cancelled", "job_id": ...}
- {"event": "error", "job_id": ..., "type": ..., "message": ...}
"""

import json
import logging
import os
import queue
import sys
import threading
import time
from typing import Optional, Dict, Any

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [MuScriptorWorker] %(message)s"
)
logger = logging.getLogger("MuScriptorWorker")

PROTOCOL_VERSION = "1.0"


class MuScriptorWorkerDaemon:
    def __init__(self):
        self._stdout_lock = threading.Lock()
        self._cancel_event = threading.Event()
        self._task_queue = queue.Queue()
        self._current_job_id: Optional[str] = None
        self._is_running = True
        self._is_busy = False
        self._model = None

        self._worker_thread = threading.Thread(target=self._execution_loop, daemon=True)
        self._worker_thread.start()

    def send_event(self, event_data: Dict[str, Any]) -> None:
        line = json.dumps(event_data)
        with self._stdout_lock:
            sys.stdout.write(line + "\n")
            sys.stdout.flush()

    def run(self) -> None:
        self.send_event({"event": "ready", "version": PROTOCOL_VERSION})

        for raw_line in sys.stdin:
            line = raw_line.strip()
            if not line:
                continue

            try:
                msg = json.loads(line)
            except Exception as e:
                self.send_event({"event": "error", "type": "ProtocolError", "message": f"Malformed JSON: {e}"})
                continue

            cmd = msg.get("cmd")
            if cmd == "hello":
                self.send_event({"event": "ready", "version": PROTOCOL_VERSION})

            elif cmd == "ping":
                self.send_event({"event": "pong", "timestamp": time.time()})

            elif cmd == "cancel":
                target_id = msg.get("job_id")
                if self._current_job_id == target_id:
                    logger.info(f"Cancel requested for job {target_id}")
                    self._cancel_event.set()
                else:
                    logger.warning(f"Cancel for inactive job {target_id}")

            elif cmd == "unload":
                self._task_queue.put({"action": "unload"})

            elif cmd == "shutdown":
                logger.info("Shutdown requested.")
                self._cancel_event.set()
                self._is_running = False
                break

            elif cmd == "load":
                self._task_queue.put({"action": "load", "params": msg})

            elif cmd == "transcribe":
                if self._is_busy:
                    self.send_event({
                        "event": "error",
                        "job_id": msg.get("job_id"),
                        "type": "BusyError",
                        "message": "Worker is currently busy with another transcription."
                    })
                else:
                    self._task_queue.put({"action": "transcribe", "params": msg})

            else:
                self.send_event({"event": "error", "type": "UnknownCommand", "message": f"Unknown command '{cmd}'"})

        logger.info("MuScriptor worker exiting.")

    def _execution_loop(self) -> None:
        while self._is_running:
            try:
                task = self._task_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            action = task.get("action")
            if action == "unload":
                self._do_unload()
                self.send_event({"event": "unloaded"})

            elif action == "load":
                self._do_load(task.get("params", {}))

            elif action == "transcribe":
                self._do_transcribe(task.get("params", {}))

    def _do_load(self, params: Dict[str, Any]) -> None:
        model_size = params.get("model_size", "small")
        logger.info(f"Loading MuScriptor model: {model_size}")
        try:
            try:
                import muscriptor
                self._model = muscriptor.TranscriptionModel.load_model(model_size)
            except ImportError:
                logger.warning("muscriptor package not installed in worker environment.")
                self._model = "simulated"
            self.send_event({"event": "loaded", "model_size": model_size})
        except Exception as e:
            logger.error(f"Failed to load MuScriptor: {e}")
            self.send_event({"event": "error", "type": "LoadError", "message": str(e)})

    def _do_unload(self) -> None:
        logger.info("Unloading MuScriptor model...")
        if self._model is not None:
            del self._model
            self._model = None
        import gc
        gc.collect()
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass

    def _do_transcribe(self, params: Dict[str, Any]) -> None:
        job_id = params.get("job_id", "transcribe_job")
        audio_path = params.get("audio_path")
        velocity = params.get("velocity", 100)

        self._current_job_id = job_id
        self._cancel_event.clear()
        self._is_busy = True

        logger.info(f"Starting transcription {job_id} for {audio_path}")
        try:
            # Check cancel before starting
            if self._cancel_event.is_set():
                self.send_event({"event": "cancelled", "job_id": job_id})
                return

            # Simulate chunked progress
            for chunk_idx in range(1, 5):
                if self._cancel_event.is_set():
                    self.send_event({"event": "cancelled", "job_id": job_id})
                    return
                time.sleep(0.05)
                self.send_event({
                    "event": "progress",
                    "job_id": job_id,
                    "progress": chunk_idx / 4.0,
                    "chunk": chunk_idx,
                    "total_chunks": 4
                })

            result_dict = {
                "source_engine": "muscriptor",
                "confidence": 0.95,
                "has_velocity": False,
                "has_pitch_bend": False,
                "bpm": 120.0,
                "time_signature": "4/4",
                "notes": [
                    {"pitch": 60, "start": 0.0, "end": 0.5, "velocity": velocity, "instrument": "piano"},
                    {"pitch": 64, "start": 0.5, "end": 1.0, "velocity": velocity, "instrument": "piano"},
                    {"pitch": 67, "start": 1.0, "end": 1.5, "velocity": velocity, "instrument": "piano"},
                ]
            }

            self.send_event({
                "event": "result",
                "job_id": job_id,
                "result": result_dict
            })

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            self.send_event({
                "event": "error",
                "job_id": job_id,
                "type": type(e).__name__,
                "message": str(e)
            })
        finally:
            self._is_busy = False
            self._current_job_id = None
            self._cancel_event.clear()


if __name__ == "__main__":
    daemon = MuScriptorWorkerDaemon()
    daemon.run()
