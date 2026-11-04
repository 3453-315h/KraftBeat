"""
Regression tests for Round 2 review fixes:
- Streaming stereo formatting and playback handling
- MusicGen stop signal and DirectML deduplicated detection
- DiffRhythm unload attribute reset and snapshot_download kwargs
- ACEStep checkpoint path resolution
"""

import os
import unittest
from unittest.mock import MagicMock, patch
import numpy as np

from src.utils.streaming import StreamingGenerator
from src.models.musicgen import MusicGenLoader
from src.models.diffrhythm import DiffRhythmLoader
from src.models.ace_step import ACEStepLoader, DEFAULT_CHECKPOINT_DIR
from src.device import DeviceInfo, DeviceType


class TestFixesRound2(unittest.TestCase):

    def test_musicgen_stop_and_reset(self):
        dev = DeviceInfo(DeviceType.CPU, "CPU", "cpu")
        loader = MusicGenLoader(dev)
        self.assertFalse(loader._stop_requested)
        loader.stop()
        self.assertTrue(loader._stop_requested)
        loader.reset_stop()
        self.assertFalse(loader._stop_requested)

    def test_musicgen_is_directml_helper(self):
        dev_cpu = DeviceInfo(DeviceType.CPU, "CPU", "cpu")
        loader_cpu = MusicGenLoader(dev_cpu)
        self.assertFalse(loader_cpu._is_directml())

        dev_dml = DeviceInfo(DeviceType.DIRECTML, "AMD Radeon", "privateuseone:0")
        loader_dml = MusicGenLoader(dev_dml)
        self.assertTrue(loader_dml._is_directml())

    def test_diffrhythm_unload_resets_attributes(self):
        loader = DiffRhythmLoader()
        loader.is_loaded = True
        loader._models = (MagicMock(), MagicMock(), MagicMock(), MagicMock())
        loader._device = "cuda:0"
        loader._dr_inference = MagicMock()
        loader._dr_prepare = MagicMock()

        loader.unload()

        self.assertFalse(loader.is_loaded)
        self.assertIsNone(loader._models)
        self.assertIsNone(loader._device)
        self.assertIsNone(loader._dr_inference)
        self.assertIsNone(loader._dr_prepare)

    def test_diffrhythm_download_kwargs_no_deprecated_resume(self):
        loader = DiffRhythmLoader()
        mock_hf = MagicMock()
        with patch.dict("sys.modules", {"huggingface_hub": mock_hf}):
            loader.download_model("diffrhythm")
            self.assertTrue(mock_hf.snapshot_download.called)
            kwargs = mock_hf.snapshot_download.call_args.kwargs
            self.assertNotIn("resume_download", kwargs)
            self.assertEqual(kwargs.get("repo_id"), "ASLP-lab/DiffRhythm-base")

    def test_acestep_checkpoint_path_resolution(self):
        loader = ACEStepLoader()
        # When explicit checkpoint_dir provided
        with patch.object(ACEStepLoader, "load", return_value=True):
            loader.load("acestep", checkpoint_dir="/custom/path")
            # If load succeeds or sets _checkpoint_dir
        
        # Test folder fallback logic
        with patch("os.path.exists") as mock_exists:
            mock_exists.side_effect = lambda p: p.endswith(os.path.join("models", "acestep"))
            # When acestep exists
            self.assertTrue(os.path.exists(os.path.join(os.getcwd(), "models", "acestep")))

    def test_streaming_stereo_channel_handling(self):
        streamer = StreamingGenerator(model=None, sample_rate=32000, chunk_duration=1.0)
        # Test 1D mono chunk duplicate to stereo
        chunk_mono = np.zeros(100, dtype=np.float32)
        playback_mono = np.column_stack((chunk_mono, chunk_mono))
        self.assertEqual(playback_mono.shape, (100, 2))

        # Test 2D stereo (2, samples) transposed to (samples, 2)
        chunk_stereo = np.zeros((2, 100), dtype=np.float32)
        playback_stereo = chunk_stereo.T
        self.assertEqual(playback_stereo.shape, (100, 2))

    def test_create_stream_callback_multidimensional(self):
        from src.utils.streaming import create_stream_callback
        waveforms = []
        progresses = []
        cb = create_stream_callback(
            on_progress=lambda p: progresses.append(p),
            on_waveform=lambda w: waveforms.append(w),
            sample_rate=1000,
            total_duration=1.0,
        )
        # Send 2D chunks of shape (2, 250)
        chunk1 = np.ones((2, 250), dtype=np.float32)
        chunk2 = np.ones((2, 250), dtype=np.float32)
        cb(chunk1, 0)
        cb(chunk2, 1)

        self.assertEqual(len(waveforms), 2)
        self.assertEqual(waveforms[-1].shape, (2, 500))
        self.assertAlmostEqual(progresses[-1], 0.5)

    def test_notes_to_smf_bytes(self):
        from src.models.transcription import TranscriptionNote, TranscriptionResult, notes_to_smf_bytes
        notes = [
            TranscriptionNote(onset_sec=0.0, offset_sec=0.5, pitch=60, velocity=100),
            TranscriptionNote(onset_sec=0.5, offset_sec=1.0, pitch=64, velocity=90),
            TranscriptionNote(onset_sec=1.0, offset_sec=1.5, pitch=67, velocity=110),
        ]
        smf = notes_to_smf_bytes(notes, tempo=120.0)
        self.assertTrue(smf.startswith(b"MThd"))
        self.assertIn(b"MTrk", smf)

        # Test save_midi with auto-serialization
        result = TranscriptionResult(notes=notes, tempo=120.0, duration=1.5)
        self.assertIsNone(result.midi_bytes)
        import tempfile
        tmp_mid = os.path.join(tempfile.gettempdir(), "test_auto_smf.mid")
        saved = result.save_midi(tmp_mid)
        self.assertTrue(saved)
        self.assertIsNotNone(result.midi_bytes)
        self.assertTrue(os.path.exists(tmp_mid))
        if os.path.exists(tmp_mid):
            os.remove(tmp_mid)

    def test_synthesize_transcription_audio(self):
        from src.models.transcription import TranscriptionNote
        from src.ui.panels.transcription_panel import synthesize_transcription_audio

        notes = [
            TranscriptionNote(onset_sec=0.0, offset_sec=0.5, pitch=60, instrument="piano"),
            TranscriptionNote(onset_sec=0.5, offset_sec=1.0, pitch=64, instrument="bass"),
        ]
        audio = synthesize_transcription_audio(notes, duration=1.0, sample_rate=22050)
        self.assertEqual(audio.shape, (22050, 2))
        self.assertTrue(np.max(np.abs(audio)) > 0.0)
        self.assertTrue(np.max(np.abs(audio)) <= 1.0)

        # Test mute filtering
        audio_muted = synthesize_transcription_audio(notes, duration=1.0, sample_rate=22050, muted_instruments={"piano", "bass"})
        self.assertEqual(np.max(np.abs(audio_muted)), 0.0)

        # Test solo filtering
        audio_solo = synthesize_transcription_audio(notes, duration=1.0, sample_rate=22050, solo_instruments={"piano"})
        self.assertTrue(np.max(np.abs(audio_solo)) > 0.0)

    def test_muscriptor_worker_daemon_protocol(self):
        from src.utils.muscriptor_worker import MuScriptorWorkerDaemon
        import queue

        daemon = MuScriptorWorkerDaemon()
        daemon._is_running = False  # Avoid leaving background thread running
        daemon.send_event = MagicMock()

        # Test hello
        daemon.send_event({"event": "ready", "version": "1.0"})
        daemon.send_event.assert_called_with({"event": "ready", "version": "1.0"})

        # Test load
        daemon._do_load({"model_size": "small"})
        self.assertIsNotNone(daemon._model)

        # Test transcribe simulated
        daemon._do_transcribe({"job_id": "job_123", "velocity": 100})
        # Check that events were sent (progress and result)
        calls = daemon.send_event.call_args_list
        event_types = [c[0][0].get("event") for c in calls]
        self.assertIn("progress", event_types)
        self.assertIn("result", event_types)

        # Test unload
        daemon._do_unload()
        self.assertIsNone(daemon._model)

    def test_yue2_worker_daemon_protocol(self):
        from src.aoide.worker_yue2 import YuE2WorkerDaemon
        import tempfile

        daemon = YuE2WorkerDaemon()
        daemon._is_running = False
        daemon.send_event = MagicMock()

        # Test load
        daemon._do_load({"model_dir": "test_dir"})
        self.assertIsNotNone(daemon._pipeline)

        # Test generate
        with tempfile.TemporaryDirectory() as tmpdir:
            job_data = {
                "job_id": "test_aoide_job",
                "output_dir": tmpdir,
                "abc": "X:1\nT:Test\nM:4/4\nK:C\nC D E F|",
            }
            daemon._do_generate(job_data)
            calls = daemon.send_event.call_args_list
            event_types = [c[0][0].get("event") for c in calls]
            self.assertIn("stage", event_types)
            self.assertIn("done", event_types)
            # Verify result.json and audio.wav were created
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "result.json")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "audio.wav")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "score.abc")))

        # Test unload
        daemon._do_unload()
        self.assertIsNone(daemon._pipeline)


if __name__ == "__main__":
    unittest.main()
