"""
Unit tests for audio effects processing chain (reverb, compression, EQ, limiter, stereo width).
"""

import unittest
import numpy as np

from src.utils.effects import (
    apply_reverb,
    apply_compression,
    apply_eq,
    apply_stereo_width,
    apply_limiter,
    apply_effects_chain,
)


class TestAudioEffects(unittest.TestCase):
    def setUp(self):
        self.sr = 32000
        # 0.5s of sine wave mono and stereo
        t = np.linspace(0, 0.5, int(self.sr * 0.5), endpoint=False)
        self.mono_audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        self.stereo_audio = np.stack([self.mono_audio, self.mono_audio * 0.8], axis=0)

    def test_reverb_identity_and_wet(self):
        # wet == 0 should return original array directly
        out_dry = apply_reverb(self.mono_audio, self.sr, wet=0.0)
        np.testing.assert_array_equal(out_dry, self.mono_audio)

        # wet > 0 should modify audio and preserve shape
        out_wet = apply_reverb(self.mono_audio, self.sr, room_size=0.3, wet=0.5)
        self.assertEqual(out_wet.shape, self.mono_audio.shape)
        self.assertFalse(np.allclose(out_wet, self.mono_audio))

        # Stereo reverb
        out_stereo = apply_reverb(self.stereo_audio, self.sr, room_size=0.3, wet=0.3)
        self.assertEqual(out_stereo.shape, self.stereo_audio.shape)

    def test_compression(self):
        # ratio <= 1.0 is identity
        out_ident = apply_compression(self.mono_audio, ratio=1.0)
        np.testing.assert_array_equal(out_ident, self.mono_audio)

        # High ratio should reduce peaks
        loud_audio = self.mono_audio * 5.0
        out_compressed = apply_compression(loud_audio, threshold_db=-10.0, ratio=8.0, sample_rate=self.sr)
        self.assertEqual(out_compressed.shape, loud_audio.shape)
        self.assertLess(np.max(np.abs(out_compressed)), np.max(np.abs(loud_audio)))

    def test_eq_3band(self):
        # Zero gains should be identity
        out_zero = apply_eq(self.mono_audio, self.sr, bass_db=0.0, mid_db=0.0, treble_db=0.0)
        np.testing.assert_array_equal(out_zero, self.mono_audio)

        # Bass boost
        out_bass = apply_eq(self.mono_audio, self.sr, bass_db=6.0, mid_db=0.0, treble_db=0.0)
        self.assertEqual(out_bass.shape, self.mono_audio.shape)

    def test_stereo_width(self):
        # 1D audio passes through untouched
        out_mono = apply_stereo_width(self.mono_audio, width=2.0)
        np.testing.assert_array_equal(out_mono, self.mono_audio)

        # Width 1.0 is identity
        out_orig = apply_stereo_width(self.stereo_audio, width=1.0)
        np.testing.assert_array_equal(out_orig, self.stereo_audio)

        # Width 0.0 collapses to mono (left == right)
        out_collapsed = apply_stereo_width(self.stereo_audio, width=0.0)
        self.assertEqual(out_collapsed.shape, self.stereo_audio.shape)
        np.testing.assert_allclose(out_collapsed[0], out_collapsed[1], atol=1e-5)

    def test_limiter(self):
        # Limiter with -6 dB ceiling (approx 0.5 linear)
        loud_audio = np.array([-2.0, -1.0, 0.0, 1.0, 2.0], dtype=np.float32)
        limited = apply_limiter(loud_audio, ceiling_db=-6.0)
        ceiling_linear = 10 ** (-6.0 / 20)
        self.assertAlmostEqual(np.max(limited), ceiling_linear, places=4)
        self.assertAlmostEqual(np.min(limited), -ceiling_linear, places=4)

    def test_effects_chain(self):
        # Run full chain
        processed = apply_effects_chain(
            self.stereo_audio,
            sample_rate=self.sr,
            reverb_wet=0.2,
            compression_ratio=2.0,
            eq_bass=2.0,
            stereo_width=1.2,
            limiter_ceiling=-1.0,
        )
        self.assertEqual(processed.shape, self.stereo_audio.shape)
        self.assertLessEqual(np.max(processed), 1.0)


if __name__ == '__main__':
    unittest.main()

