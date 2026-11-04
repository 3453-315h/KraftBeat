"""
Unit tests for audio processing and I/O utilities.
"""

import unittest
import tempfile
from pathlib import Path
import numpy as np
import soundfile as sf
from unittest.mock import patch

from src.utils.audio import save_audio, load_audio, get_duration, normalize_audio, crossfade_audio


class TestAudioUtils(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_wav(self):
        sr = 32000
        # 1 second of 440Hz sine wave (mono)
        t = np.linspace(0, 1.0, sr, endpoint=False)
        audio = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
        
        target_path = self.test_dir / "test.wav"
        saved_path = save_audio(audio, str(target_path), sample_rate=sr, audio_format="wav")
        
        self.assertIsNotNone(saved_path)
        self.assertEqual(saved_path, str(target_path))
        self.assertTrue(Path(saved_path).exists())
        
        # Load and verify
        loaded_audio, loaded_sr = load_audio(saved_path)
        self.assertEqual(loaded_sr, sr)
        self.assertEqual(len(loaded_audio), sr)

    def test_save_audio_channels_first_transpose(self):
        sr = 32000
        # Stereo (2, 32000)
        audio_2d = np.zeros((2, sr), dtype=np.float32)
        target_path = self.test_dir / "stereo.wav"
        saved_path = save_audio(audio_2d, str(target_path), sample_rate=sr)
        
        self.assertIsNotNone(saved_path)
        info = sf.info(saved_path)
        self.assertEqual(info.channels, 2)
        self.assertEqual(info.frames, sr)

    def test_save_audio_lossy_fallback_truthfulness(self):
        sr = 32000
        audio = np.zeros(sr, dtype=np.float32)
        target_path = self.test_dir / "music.mp3"
        
        # Simulate pydub missing
        with patch.dict('sys.modules', {'pydub': None}):
            saved_path = save_audio(audio, str(target_path), sample_rate=sr, audio_format="mp3")
            
        self.assertIsNotNone(saved_path)
        # Truthful check: must have fallen back to .wav, NOT claimed .mp3!
        self.assertTrue(saved_path.endswith(".wav"))
        self.assertTrue(Path(saved_path).exists())
        self.assertFalse(target_path.exists())

    def test_save_audio_failure(self):
        # Invalid path (directory that doesn't exist and cannot be written)
        invalid_path = "/nonexistent_dir_12345/unwritable_file.wav"
        saved_path = save_audio(np.zeros(100), invalid_path)
        self.assertIsNone(saved_path)

    def test_normalize_audio(self):
        audio = np.array([0.1, -0.5, 0.2], dtype=np.float32)
        normalized = normalize_audio(audio, target_db=0.0)
        # Peak should be ~1.0 (0 dB)
        self.assertAlmostEqual(np.max(np.abs(normalized)), 1.0, places=4)

    def test_get_duration(self):
        sr = 32000
        audio_1s = np.zeros(sr)
        self.assertEqual(get_duration(audio_1s, sr), 1.0)
        
        # 2D stereo (2, 64000) -> 2 seconds
        audio_2s = np.zeros((2, 64000))
        self.assertEqual(get_duration(audio_2s, sr), 2.0)

    def test_crossfade_audio_1d(self):
        # 100 samples each, crossfade of 20 samples -> total output 180 samples
        a1 = np.ones(100, dtype=np.float32)
        a2 = np.ones(100, dtype=np.float32) * 2.0
        
        # Equal power
        res = crossfade_audio(a1, a2, crossfade_samples=20, curve="equal_power")
        self.assertEqual(len(res), 180)
        self.assertAlmostEqual(res[0], 1.0)
        self.assertAlmostEqual(res[-1], 2.0)

        # Linear
        res_lin = crossfade_audio(a1, a2, crossfade_samples=20, curve="linear")
        self.assertEqual(len(res_lin), 180)

    def test_crossfade_audio_2d_channels_first(self):
        # (2, 100) and (2, 100) with 20 crossfade -> (2, 180)
        a1 = np.ones((2, 100), dtype=np.float32)
        a2 = np.ones((2, 100), dtype=np.float32) * 3.0
        res = crossfade_audio(a1, a2, crossfade_samples=20)
        self.assertEqual(res.shape, (2, 180))

    def test_crossfade_audio_mono_stereo_broadcasting(self):
        # a1 is mono (1, 100), a2 is stereo (2, 100)
        a1 = np.ones((1, 100), dtype=np.float32)
        a2 = np.ones((2, 100), dtype=np.float32) * 2.0
        res = crossfade_audio(a1, a2, crossfade_samples=20)
        self.assertEqual(res.shape, (2, 180))

    def test_crossfade_boundary_and_empty(self):
        a1 = np.ones(50, dtype=np.float32)
        a2 = np.ones(50, dtype=np.float32)
        
        # Zero crossfade -> simple concat (100)
        res_zero = crossfade_audio(a1, a2, crossfade_samples=0)
        self.assertEqual(len(res_zero), 100)
        
        # Crossfade exceeds segment length -> simple concat
        res_exceed = crossfade_audio(a1, a2, crossfade_samples=60)
        self.assertEqual(len(res_exceed), 100)

        # None / empty handling
        self.assertEqual(len(crossfade_audio(None, a2, 10)), 50)
        self.assertEqual(len(crossfade_audio(a1, None, 10)), 50)


if __name__ == '__main__':
    unittest.main()
