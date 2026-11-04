"""
Unit tests for Audio-to-MIDI Multi-Engine Dispatcher and Transcription Model.
"""

import unittest
from unittest.mock import MagicMock, patch
import tempfile
from pathlib import Path

from src.models.transcription import TranscriptionNote, TranscriptionResult
from src.utils.midi import transcribe_audio, audio_to_midi


class TestMIDI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_transcription_result_model(self):
        notes = [
            TranscriptionNote(onset_sec=0.0, offset_sec=0.5, pitch=60, instrument="piano", velocity=80),
            TranscriptionNote(onset_sec=0.5, offset_sec=1.0, pitch=62, instrument="bass", velocity=90),
        ]
        result = TranscriptionResult(
            notes=notes,
            tempo=128.0,
            duration=1.0,
            engine_id="basic-pitch",
            has_velocity=True,
            has_pitch_bend=True,
            midi_bytes=b"MThd...",
        )
        self.assertEqual(result.get_instruments(), ["piano", "bass"])
        self.assertEqual(len(result.get_notes_for_instrument("piano")), 1)

        # Test save_midi
        out_mid = self.test_dir / "test.mid"
        ok = result.save_midi(str(out_mid))
        self.assertTrue(ok)
        self.assertEqual(out_mid.read_bytes(), b"MThd...")

    def test_invalid_engine_returns_none(self):
        result = transcribe_audio("some_audio.wav", engine="invalid_engine_xyz")
        self.assertIsNone(result)

    def test_zero_silent_fallback_on_muscriptor_failure(self):
        # Simulate muscriptor failing
        with patch("src.utils.midi_muscriptor.transcribe_muscriptor", return_value=None) as mock_muscriptor:
            with patch("src.utils.midi.transcribe_basic_pitch") as mock_bp:
                result = transcribe_audio("some_audio.wav", engine="muscriptor")
                self.assertIsNone(result)
                mock_muscriptor.assert_called_once()
                # Crucial rule: must NOT fall back to basic_pitch
                mock_bp.assert_not_called()

    def test_muscriptor_capability_contract(self):
        # When muscriptor runs, capability contract requires has_velocity=False, has_pitch_bend=False
        dummy_result = TranscriptionResult(
            notes=[TranscriptionNote(0.0, 1.0, 60, "piano", velocity=None, pitch_bend=None)],
            tempo=120.0,
            duration=1.0,
            engine_id="muscriptor",
            has_velocity=False,
            has_pitch_bend=False,
            midi_bytes=b"MThd...",
        )
        with patch("src.utils.midi_muscriptor.transcribe_muscriptor", return_value=dummy_result):
            res = transcribe_audio("audio.wav", engine="muscriptor")
            self.assertIsNotNone(res)
            self.assertFalse(res.has_velocity)
            self.assertFalse(res.has_pitch_bend)
            self.assertIsNone(res.notes[0].velocity)

    def test_audio_to_midi_convenience_helper(self):
        target_mid = self.test_dir / "out.mid"
        target_mid.write_bytes(b"dummy_midi")
        dummy_res = TranscriptionResult(
            notes=[],
            tempo=120.0,
            duration=1.0,
            engine_id="basic-pitch",
            midi_bytes=b"dummy_midi",
        )
        with patch("src.utils.midi.transcribe_audio", return_value=dummy_res):
            out_path = audio_to_midi("audio.wav", str(target_mid))
            self.assertEqual(out_path, str(target_mid))


if __name__ == '__main__':
    unittest.main()
