import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import unittest
from pathlib import Path
from PyQt6.QtWidgets import QApplication

_qapp = QApplication.instance() or QApplication(["test_aoide"])

from src.aoide.backend import (
    AoideJob,
    AoideJobStatus,
    YuE2PackageBackend,
    ComfyUIBackend,
    get_aoide_backend,
)
from src.aoide.abc_tools import validate_abc, convert_to_instrumental
from src.models.catalog import MODEL_CATALOG
from src.models.base import get_backend
from src.models.yue2 import YuE2Loader
from src.ui.panels.aoide_panel import AoidePanel


class TestAoideIntegration(unittest.TestCase):
    def test_job_id_validation(self):
        # Valid IDs: [A-Za-z0-9][A-Za-z0-9_.-]{0,179}
        valid_job = AoideJob(job_id="job_123.abc-45", style="pop")
        self.assertTrue(valid_job.validate_id())

        # Invalid IDs
        invalid_job1 = AoideJob(job_id="-leading_hyphen", style="pop")
        self.assertFalse(invalid_job1.validate_id())

        invalid_job2 = AoideJob(job_id="has spaces", style="pop")
        self.assertFalse(invalid_job2.validate_id())

        invalid_job3 = AoideJob(job_id="", style="pop")
        self.assertFalse(invalid_job3.validate_id())

    def test_abc_validation(self):
        valid_abc = "X:1\nT:Test\nM:4/4\nL:1/8\nK:C\nC D E F | G2 G2 |"
        valid, msg = validate_abc(valid_abc)
        self.assertTrue(valid)

        invalid_abc = "T:No Key Header\nC D E F"
        valid, msg = validate_abc(invalid_abc)
        self.assertFalse(valid)
        self.assertIn("Key", msg)

    def test_instrumental_preservation_gate(self):
        score_with_vocals = (
            "X:1\nT:Song With Vocals\nM:4/4\nL:1/8\nK:G\n"
            "[V:Vocal] G A B c | d2 d2 |\n"
            "w: Sing-ing a song of love\n"
            "[V:Ins] [G4B4] | [G4B4] |\n"
        )
        success, inst_abc, status = convert_to_instrumental(score_with_vocals)
        self.assertTrue(success)
        self.assertIn("instrumental-conditioned", status)
        self.assertNotIn("w:", inst_abc)
        self.assertNotIn("Sing-ing", inst_abc)
        self.assertNotIn("[V:Vocal]", inst_abc)
        self.assertIn("[V:Ins]", inst_abc)

    def test_model_catalog_yue2_entries(self):
        self.assertIn("yue2-3b", MODEL_CATALOG)
        self.assertIn("yue2-vae", MODEL_CATALOG)
        self.assertIn("yue2-comfy-int8", MODEL_CATALOG)

        entry = MODEL_CATALOG["yue2-3b"]
        self.assertEqual(entry["family"], "YUE2")
        self.assertEqual(entry["id"], "m-a-p/YuE2-3B")

    def test_backend_registry_yue2(self):
        backend = get_backend("yue2")
        self.assertIsInstance(backend, YuE2Loader)
        self.assertEqual(backend.sample_rate, 48000)
        self.assertTrue(backend.supports_vocals)
        self.assertTrue(backend.supports_lyrics)
        self.assertFalse(backend.supports_continuation)

    def test_aoide_panel_ui(self):
        panel = AoidePanel()
        panel.show()
        self.assertIsNotNone(panel.route_combo)
        self.assertIsNotNone(panel.style_input)
        self.assertIsNotNone(panel.lyrics_input)

        # Route 1: Duration container is hidden
        self.assertEqual(panel.route_combo.currentIndex(), 0)
        self.assertTrue(panel.duration_container.isHidden())

        # Route 2 (ComfyUI): Duration container becomes visible
        panel.route_combo.setCurrentIndex(1)
        self.assertFalse(panel.duration_container.isHidden())

        # Style preset insertion
        panel.preset_combo.setCurrentText("Modern Pop")
        self.assertIn("modern pop", panel.style_input.toPlainText())

        panel.close()

    def test_yue2_download_model(self):
        from unittest.mock import patch, MagicMock
        loader = YuE2Loader()

        mock_hf = MagicMock()
        with patch.dict("sys.modules", {"huggingface_hub": mock_hf}):
            # Valid catalog key
            ok = loader.download_model("yue2-3b")
            self.assertTrue(ok)
            self.assertTrue(mock_hf.snapshot_download.called)
            kwargs = mock_hf.snapshot_download.call_args.kwargs
            self.assertEqual(kwargs.get("repo_id"), "m-a-p/YuE2-3B")

            # Unknown model
            ok_unknown = loader.download_model("nonexistent_model_xyz")
            self.assertFalse(ok_unknown)


if __name__ == '__main__':
    unittest.main()
