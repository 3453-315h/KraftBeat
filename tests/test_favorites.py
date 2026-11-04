"""
Regression tests for Favorites toggle handling.
"""

import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import unittest
from unittest.mock import MagicMock, patch
import tempfile
from pathlib import Path
import numpy as np

from PyQt6.QtWidgets import QApplication, QPushButton, QStatusBar
from src.ui.main_window import MainWindow

_qapp = QApplication.instance() or QApplication(["test_app"])


class TestFavorites(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.outputs_dir = Path(self.temp_dir.name) / "outputs"
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

        # Mock minimal MainWindow instance without running full init
        self.window = MagicMock(spec=MainWindow)
        self.window.outputs_dir = self.outputs_dir
        self.window.fav_btn = QPushButton()
        self.window.fav_btn.setCheckable(True)
        self.window.status_bar = QStatusBar()
        self.window.current_sample_rate = 32000

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_favorite_toggle_no_audio(self):
        self.window.current_audio = None
        self.window.fav_btn.setChecked(True)

        MainWindow.toggle_favorite(self.window)

        # Should revert check state and inform user
        self.assertFalse(self.window.fav_btn.isChecked())
        self.assertIn("No audio", self.window.status_bar.currentMessage())

    def test_favorite_toggle_with_audio_success(self):
        self.window.current_audio = np.zeros(32000, dtype=np.float32)
        self.window.fav_btn.setChecked(True)

        with patch("src.ui.main_window.save_audio", return_value="/path/fav.wav") as mock_save:
            MainWindow.toggle_favorite(self.window)
            self.assertTrue(mock_save.called)
            # Verify save_audio was called with audio first, path second, sample rate third
            args, _ = mock_save.call_args
            self.assertIs(args[0], self.window.current_audio)
            self.assertIn("fav_", args[1])
            self.assertEqual(args[2], 32000)

        self.assertEqual(self.window.fav_btn.text(), "🌟")
        self.assertIn("Added to favorites", self.window.status_bar.currentMessage())

    def test_favorite_toggle_uncheck(self):
        self.window.fav_btn.setChecked(False)

        MainWindow.toggle_favorite(self.window)

        self.assertEqual(self.window.fav_btn.text(), "⭐")
        self.assertIn("Removed from favorites", self.window.status_bar.currentMessage())


if __name__ == '__main__':
    unittest.main()
