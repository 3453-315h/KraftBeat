"""
Unit tests for Vocal and Full-Song Generation Engines (ACE-Step, DiffRhythm, YuE2).
"""

import unittest
from unittest.mock import MagicMock, patch
import numpy as np

from src.models.ace_step import ACEStepLoader
from src.models.diffrhythm import DiffRhythmLoader
from src.models.yue2 import YuE2Loader
from src.models.catalog import MODEL_CATALOG


class TestVocalEngines(unittest.TestCase):
    def test_ace_step_contracts(self):
        loader = ACEStepLoader()
        self.assertTrue(loader.supports_vocals)
        self.assertTrue(loader.supports_lyrics)
        self.assertFalse(loader.supports_continuation)
        self.assertEqual(loader.max_duration, 240.0)
        self.assertEqual(loader.sample_rate, 44100)
        self.assertEqual(loader.backend_name, "ACE-Step")

        # Stop signal
        self.assertFalse(loader._stop_requested)
        loader.stop()
        self.assertTrue(loader._stop_requested)
        loader.reset_stop()
        self.assertFalse(loader._stop_requested)

    def test_ace_step_download_kwargs_no_deprecated_resume(self):
        loader = ACEStepLoader()
        mock_hf = MagicMock()
        with patch.dict("sys.modules", {"huggingface_hub": mock_hf}):
            loader.download_model("acestep")
            self.assertTrue(mock_hf.snapshot_download.called)
            kwargs = mock_hf.snapshot_download.call_args.kwargs
            self.assertNotIn("resume_download", kwargs)
            self.assertEqual(kwargs.get("repo_id"), "ACE-Step/ACE-Step-v1-3.5B")

    def test_ace_step_generate_output_shaping(self):
        loader = ACEStepLoader()
        loader.is_loaded = True
        loader._pipeline = MagicMock()

        mock_torch = MagicMock()
        mock_torch.cuda.is_available.return_value = False
        with patch.dict("sys.modules", {"torch": mock_torch}):
            # 1. Pipeline returns 1D mono audio (samples,) -> should reshape to (2, samples)
            loader._pipeline.return_value = np.zeros(1000, dtype=np.float32)
            res = loader.generate(prompt="pop song", duration=30.0)
            self.assertIsNotNone(res)
            self.assertEqual(res.shape, (2, 1000))

            # 2. Pipeline returns (samples, 2) -> should transpose to (2, samples)
            loader._pipeline.return_value = np.zeros((1000, 2), dtype=np.float32)
            res_transposed = loader.generate(prompt="pop song", duration=30.0)
            self.assertEqual(res_transposed.shape, (2, 1000))

            # 3. Pipeline returns 3D (1, 2, samples) -> should squeeze batch dim to (2, samples)
            loader._pipeline.return_value = np.zeros((1, 2, 1000), dtype=np.float32)
            res_3d = loader.generate(prompt="pop song", duration=30.0)
            self.assertEqual(res_3d.shape, (2, 1000))

    def test_diffrhythm_contracts(self):
        loader = DiffRhythmLoader()
        self.assertTrue(loader.supports_vocals)
        self.assertTrue(loader.supports_lyrics)
        self.assertTrue(loader.supports_continuation)
        self.assertEqual(loader.max_duration, 285.0)
        self.assertEqual(loader.sample_rate, 44100)
        self.assertEqual(loader.backend_name, "DiffRhythm")

        # Stop signal
        self.assertFalse(loader._stop_requested)
        loader.stop()
        self.assertTrue(loader._stop_requested)
        loader.reset_stop()
        self.assertFalse(loader._stop_requested)

    def test_diffrhythm_download_kwargs(self):
        loader = DiffRhythmLoader()
        mock_hf = MagicMock()
        with patch.dict("sys.modules", {"huggingface_hub": mock_hf}):
            loader.download_model("diffrhythm")
            self.assertTrue(mock_hf.snapshot_download.called)
            kwargs = mock_hf.snapshot_download.call_args.kwargs
            self.assertNotIn("resume_download", kwargs)
            self.assertEqual(kwargs.get("repo_id"), "ASLP-lab/DiffRhythm-base")

    def test_diffrhythm_lyrics_auto_timestamp(self):
        loader = DiffRhythmLoader()
        loader.is_loaded = True
        loader._device = "cpu"
        loader.code_path = "/tmp"
        loader.max_frames = 2048
        loader._models = (MagicMock(), MagicMock(), MagicMock(), MagicMock())
        loader._cwd_ctx = MagicMock()
        
        # Mock infer functions
        loader._dr_lrc = MagicMock(return_value=("mock_lrc", 0, 100, 95))
        loader._dr_style = MagicMock(return_value="mock_style")
        loader._dr_neg = MagicMock(return_value="mock_neg")
        loader._dr_ref = MagicMock(return_value=("mock_latent", 100))
        loader._dr_inference = MagicMock(return_value=[np.zeros((2, 1000), dtype=np.float32)])

        # Generate without lyrics -> should auto-format timestamp prefix
        loader.generate(prompt="electronic dance", lyrics=None)
        called_lyrics = loader._dr_lrc.call_args[0][1]
        self.assertEqual(called_lyrics, "[00:00.00]electronic dance")

    def test_yue2_loader_contracts_and_routes(self):
        # Route 1: package
        loader_pkg = YuE2Loader(route="package")
        self.assertTrue(loader_pkg.supports_vocals)
        self.assertTrue(loader_pkg.supports_lyrics)
        self.assertEqual(loader_pkg.sample_rate, 48000)
        self.assertEqual(loader_pkg.max_duration, 900.0)

        # Route 2: comfyui
        loader_comfy = YuE2Loader(route="comfyui")
        self.assertEqual(loader_comfy.route, "comfyui")


if __name__ == '__main__':
    unittest.main()
