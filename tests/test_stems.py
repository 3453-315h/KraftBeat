"""
Unit tests for Demucs stems separation and file export.
"""

import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import tempfile
import numpy as np

from src.utils.stems import (
    separate_stems,
    save_stems,
    separate_file,
    get_available_models,
    STEM_NAMES,
)


class TestStems(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_available_models(self):
        models = get_available_models()
        self.assertGreaterEqual(len(models), 3)
        model_names = [m["name"] for m in models]
        self.assertIn("htdemucs", model_names)
        self.assertIn("htdemucs_ft", model_names)

    def test_save_stems(self):
        stems = {
            "drums": np.zeros((2, 1000), dtype=np.float32),
            "bass": np.zeros((2, 1000), dtype=np.float32),
            "vocals": np.zeros((2, 1000), dtype=np.float32),
            "other": np.zeros((2, 1000), dtype=np.float32),
        }
        saved = save_stems(stems, str(self.output_dir), sample_rate=44100, audio_format="wav")
        self.assertEqual(len(saved), 4)
        for name in STEM_NAMES:
            self.assertIn(name, saved)
            self.assertTrue(Path(saved[name]).exists())
            self.assertTrue(saved[name].endswith(f"{name}.wav"))

    def test_separate_stems_missing_demucs_returns_none(self):
        with patch("src.utils.stems.DEMUCS_AVAILABLE", False):
            result = separate_stems(np.zeros(1000))
            self.assertIsNone(result)

    def test_separate_file_delegation(self):
        dummy_wav = self.output_dir / "input.wav"
        dummy_wav.write_bytes(b"dummy")

        with patch("src.utils.audio.load_audio", return_value=(np.zeros((2, 44100)), 44100)):
            dummy_stems = {name: np.zeros((2, 44100)) for name in STEM_NAMES}
            with patch("src.utils.stems.separate_stems", return_value=dummy_stems) as mock_sep:
                res = separate_file(str(dummy_wav), output_dir=str(self.output_dir / "stems_out"))
                self.assertIsNotNone(res)
                mock_sep.assert_called_once()
                self.assertEqual(len(res), 4)


if __name__ == '__main__':
    unittest.main()

