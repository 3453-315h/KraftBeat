import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import unittest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QPoint

_qapp = QApplication.instance() or QApplication(["test_transcription_ui"])

from src.models.transcription import TranscriptionNote, TranscriptionResult
from src.ui.panels.transcription_panel import PianoRollCanvas, TranscriptionDialog


class TestTranscriptionUI(unittest.TestCase):
    def setUp(self):
        self.sample_notes = [
            TranscriptionNote(onset_sec=0.0, offset_sec=1.0, pitch=60, instrument="piano", velocity=100),
            TranscriptionNote(onset_sec=1.0, offset_sec=2.0, pitch=64, instrument="guitar", velocity=100),
            TranscriptionNote(onset_sec=2.0, offset_sec=3.0, pitch=67, instrument="bass", velocity=100),
        ]
        self.result = TranscriptionResult(
            notes=self.sample_notes,
            duration=4.0,
            tempo=120.0,
            time_signature="4/4",
            engine_id="muscriptor",
            has_velocity=False,
            has_pitch_bend=False,
        )

    def test_canvas_note_rendering_and_geometry(self):
        canvas = PianoRollCanvas()
        canvas.resize(800, 400)
        canvas.set_transcription(self.result)

        self.assertEqual(len(canvas.result.notes), 3)
        self.assertEqual(canvas.total_duration_sec, 4.0)

        # Coordinate conversion
        x_start = canvas.time_to_x(0.0)
        self.assertEqual(x_start, canvas.gutter_width)
        
        t_recovered = canvas.x_to_time(x_start)
        self.assertAlmostEqual(t_recovered, 0.0, places=2)

        # Pitch to Y
        y_c4 = canvas.pitch_to_y(60)
        self.assertGreaterEqual(y_c4, 0)
        p_recovered = canvas.y_to_pitch(y_c4)
        self.assertEqual(p_recovered, 60)

    def test_canvas_mute_and_solo_filtering(self):
        canvas = PianoRollCanvas()
        canvas.set_transcription(self.result)

        # Default: all unmuted
        self.assertTrue(canvas.is_note_visible(self.sample_notes[0]))
        self.assertTrue(canvas.is_note_visible(self.sample_notes[1]))

        # Mute piano
        canvas.set_instrument_mute("piano", True)
        self.assertFalse(canvas.is_note_visible(self.sample_notes[0]))
        self.assertTrue(canvas.is_note_visible(self.sample_notes[1]))

        # Solo guitar
        canvas.set_instrument_solo("guitar", True)
        self.assertFalse(canvas.is_note_visible(self.sample_notes[0]))  # muted & not solo
        self.assertTrue(canvas.is_note_visible(self.sample_notes[1]))   # solo
        self.assertFalse(canvas.is_note_visible(self.sample_notes[2]))  # not solo

    def test_dialog_instantiation_and_widgets(self):
        dialog = TranscriptionDialog(result=self.result, midi_path="/tmp/test.mid")
        self.assertIsNotNone(dialog.piano_roll)
        self.assertIsNotNone(dialog.blend_slider)
        self.assertIsNotNone(dialog.export_btn)
        self.assertEqual(len(dialog.instrument_strips), 3)
        self.assertIn("piano", dialog.instrument_strips)
        self.assertIn("guitar", dialog.instrument_strips)
        self.assertIn("bass", dialog.instrument_strips)
        dialog.close()

    def test_player_panel_transcription_button(self):
        from src.ui.panels.player_panel import PlayerPanel
        from unittest.mock import patch, MagicMock
        import numpy as np

        panel = PlayerPanel()
        self.assertFalse(panel.transcribe_btn.isEnabled())

        # When audio is set, button should be enabled
        audio_data = np.zeros(16000, dtype=np.float32)
        panel.set_audio(audio_data, 16000)
        self.assertTrue(panel.transcribe_btn.isEnabled())

        # Test triggering transcription with mock
        with patch("src.utils.midi.transcribe_audio", return_value=self.result) as mock_transcribe:
            with patch.object(TranscriptionDialog, "exec", return_value=None) as mock_exec:
                panel.transcribe_audio_to_midi()
                mock_transcribe.assert_called_once()
                mock_exec.assert_called_once()


if __name__ == '__main__':
    unittest.main()
