"""
Kraftbeat API Worker

A QThread that runs the FastAPI/Uvicorn server in the background
so the PyQt6 UI remains fully responsive while the API is served.
"""

import logging
from PyQt6.QtCore import QThread, pyqtSignal

from utils.config import get_config

logger = logging.getLogger(__name__)

DEFAULT_HOST = get_config("api_host", "127.0.0.1")
DEFAULT_PORT = get_config("api_port", 8765)


class APIWorker(QThread):
    """
    Runs the Uvicorn ASGI server on a background thread.
    The server can be started and stopped cleanly alongside the main app.
    """
    started_ok = pyqtSignal(str)   # Emits the server URL on success
    error = pyqtSignal(str)        # Emits error message on failure

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = port
        self._server = None
        self._loop = None

    def run(self):
        """Entry point for the thread — starts the async event loop + server."""
        try:
            import uvicorn
            import asyncio
            from api.server import create_app

            app = create_app()
            if app is None:
                self.error.emit("FastAPI/Uvicorn not installed. Run: pip install fastapi uvicorn[standard]")
                return

            config = uvicorn.Config(
                app,
                host=self.host,
                port=self.port,
                log_level="warning",   # Keep noise down in the Kraftbeat console
                access_log=False,
            )
            self._server = uvicorn.Server(config)

            # Notify UI that the API is live
            url = f"http://{self.host}:{self.port}"
            self.started_ok.emit(url)
            logger.info(f"Kraftbeat API running → {url}/docs")

            # Block this thread running the async server
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._server.serve())

        except OSError as e:
            # Port already in use or similar
            self.error.emit(f"API failed to start (port {self.port} may be in use): {e}")
        except Exception as e:
            logger.error(f"API Worker error: {e}")
            self.error.emit(str(e))

    def stop(self):
        """Gracefully shut down the Uvicorn server."""
        if self._server:
            self._server.should_exit = True
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        self.wait(3000)
