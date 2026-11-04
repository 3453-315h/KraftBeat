"""
Unit tests for REST API endpoints and generation worker.
"""

import unittest
from unittest.mock import MagicMock, patch
import numpy as np
from fastapi.testclient import TestClient

from src.api.server import create_app, set_loader, get_state, _state, _state_lock, _run_generation


class TestAPIServer(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = TestClient(self.app)
        # Reset state
        with _state_lock:
            _state["loader"] = None
            _state["is_generating"] = False
            _state["current_job_id"] = None
            _state["current_status"] = "idle"
            _state["current_progress"] = 0
            _state["last_output_path"] = None
            _state["start_time"] = None
            _state["stop_requested"] = False

    def test_root_health_check(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("name"), "Kraftbeat API")
        self.assertEqual(data.get("status"), "running")

    def test_get_status_idle(self):
        response = self.client.get("/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "idle")
        self.assertFalse(data.get("is_generating"))

    def test_generate_without_loader_returns_503(self):
        response = self.client.post("/generate", json={"prompt": "ambient chill", "duration": 10})
        self.assertEqual(response.status_code, 503)
        self.assertIn("No model is loaded", response.json()["detail"])

    def test_run_generation_success(self):
        mock_loader = MagicMock()
        mock_loader.model = True
        mock_loader.sample_rate = 32000
        # Generate 1 sec audio
        mock_loader.generate.return_value = np.zeros(32000, dtype=np.float32)
        set_loader(mock_loader)

        # Create dummy request object
        class DummyReq:
            prompt = "lofi hip hop beat"
            duration = 10
            temperature = 1.0
            top_k = 250
            top_p = 0.0
            cfg_coef = 3.0

        with patch("soundfile.write") as mock_sf_write:
            _run_generation(DummyReq(), "test1234")

        # Verify loader was called with correct parameters without infinite_mode or use_cache
        mock_loader.generate.assert_called_once_with(
            prompt="lofi hip hop beat",
            duration=10,
            temperature=1.0,
            top_k=250,
            top_p=0.0,
            cfg_coef=3.0,
            progress_callback=unittest.mock.ANY,
        )
        state = get_state()
        self.assertEqual(state["current_status"], "complete")
        self.assertEqual(state["current_progress"], 100)
        self.assertFalse(state["is_generating"])
        self.assertIsNotNone(state["last_output_path"])

    def test_run_generation_save_failure_reports_error(self):
        mock_loader = MagicMock()
        mock_loader.model = True
        mock_loader.sample_rate = 32000
        mock_loader.generate.return_value = np.zeros(32000, dtype=np.float32)
        set_loader(mock_loader)

        class DummyReq:
            prompt = "synthwave drive"
            duration = 5
            temperature = 1.0
            top_k = 250
            top_p = 0.0
            cfg_coef = 3.0

        # Simulate soundfile write failure
        with patch("soundfile.write", side_effect=OSError("Disk full")):
            _run_generation(DummyReq(), "fail1234")

        state = get_state()
        self.assertEqual(state["current_status"], "error")
        self.assertFalse(state["is_generating"])
        self.assertIsNone(state["last_output_path"])

    def test_get_status_by_job_id(self):
        from src.api.server import _jobs
        _jobs["job_abc"] = {
            "job_id": "job_abc",
            "is_generating": False,
            "status": "complete",
            "progress": 100,
            "elapsed_seconds": 12.5,
            "output_path": "/tmp/out.wav",
        }
        resp = self.client.get("/status?job_id=job_abc")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "complete")

        resp_404 = self.client.get("/status?job_id=nonexistent")
        self.assertEqual(resp_404.status_code, 404)

    def test_stop_generation_calls_loader_stop(self):
        mock_loader = MagicMock()
        mock_loader.model = True
        set_loader(mock_loader)

        with _state_lock:
            _state["is_generating"] = True
            _state["current_job_id"] = "job_stop"

        resp = self.client.post("/stop")
        self.assertEqual(resp.status_code, 200)
        mock_loader.stop.assert_called_once()
        state = get_state()
        self.assertTrue(state["stop_requested"])
        self.assertEqual(state["current_status"], "stopping")


if __name__ == '__main__':
    unittest.main()
