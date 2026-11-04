"""
Kraftbeat Audio-to-MIDI Multi-Engine Dispatcher.

Supports polyphonic transcription via Spotify's basic-pitch and Kyutai's MuScriptor.
Enforces an explicit zero-silent-fallback policy: if the selected engine fails,
it errors clearly and never quietly substitutes another engine's output.
"""

import logging
import os
from pathlib import Path
from typing import Optional, Callable, List

from src.models.transcription import TranscriptionNote, TranscriptionResult
from src.utils.config import get_config

logger = logging.getLogger(__name__)


def transcribe_basic_pitch(
    audio_path: str,
    output_path: Optional[str] = None,
    progress_callback: Optional[Callable[[float, str], None]] = None,
) -> Optional[TranscriptionResult]:
    """
    Transcribe audio to MIDI using Spotify's basic-pitch.
    Recovers dynamics (velocity) and pitch bends.
    """
    try:
        from basic_pitch.inference import predict
    except ImportError:
        logger.error("basic-pitch is not installed. Please run: pip install basic-pitch")
        return None

    try:
        if progress_callback:
            progress_callback(0.1, "Analyzing audio with basic-pitch...")

        logger.info(f"Extracting MIDI with basic-pitch from {audio_path}...")
        model_output, midi_data, note_events = predict(audio_path)

        if progress_callback:
            progress_callback(0.7, "Processing note events...")

        notes: List[TranscriptionNote] = []
        for event in note_events:
            # note_events: list of (start_time, end_time, pitch, amplitude, pitch_bends)
            start_time = float(event[0])
            end_time = float(event[1])
            pitch = int(event[2])
            amplitude = float(event[3])
            velocity = int(min(max(amplitude * 127, 1), 127))
            bends = [int(b) for b in event[4]] if len(event) > 4 and event[4] else None

            notes.append(
                TranscriptionNote(
                    onset_sec=start_time,
                    offset_sec=end_time,
                    pitch=pitch,
                    instrument="acoustic_grand_piano",
                    velocity=velocity,
                    pitch_bend=bends,
                )
            )

        # Estimate tempo and duration
        duration = 0.0
        tempo = 120.0
        if midi_data:
            duration = midi_data.get_end_time()
            tempos, times = midi_data.get_tempo_changes()
            if len(tempos) > 0:
                tempo = float(tempos[0])

        midi_bytes = None
        if output_path is None:
            base, _ = os.path.splitext(audio_path)
            output_path = f"{base}.mid"

        if midi_data:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            midi_data.write(output_path)
            with open(output_path, "rb") as f:
                midi_bytes = f.read()

        if progress_callback:
            progress_callback(1.0, "Transcription complete")

        return TranscriptionResult(
            notes=notes,
            tempo=tempo,
            time_signature=None,
            is_placeholder_grid=False,
            duration=duration,
            source_audio_path=audio_path,
            engine_id="basic-pitch",
            model_size=None,
            has_velocity=True,
            has_pitch_bend=True,
            midi_bytes=midi_bytes,
        )

    except Exception as e:
        logger.error(f"basic-pitch transcription failed: {e}")
        return None


def transcribe_audio(
    audio_path: str,
    output_path: Optional[str] = None,
    engine: Optional[str] = None,
    model_size: str = "small",
    progress_callback: Optional[Callable[[float, str], None]] = None,
) -> Optional[TranscriptionResult]:
    """
    Main transcription dispatcher.
    
    Args:
        audio_path: Path to source audio file
        output_path: Optional path for destination .mid file
        engine: Explicit engine choice ('basic-pitch' | 'muscriptor'). Defaults to settings.
        model_size: Model size for muscriptor ('small' | 'medium' | 'large')
        progress_callback: Optional progress reporter callback
        
    Returns:
        TranscriptionResult or None on failure. No silent cross-engine fallback.
    """
    selected_engine = (engine or get_config("transcription_engine", "basic-pitch")).lower()

    if selected_engine == "muscriptor":
        from src.utils.midi_muscriptor import transcribe_muscriptor
        return transcribe_muscriptor(
            audio_path=audio_path,
            output_path=output_path,
            model_size=model_size,
            progress_callback=progress_callback
        )
    elif selected_engine == "basic-pitch":
        return transcribe_basic_pitch(
            audio_path=audio_path,
            output_path=output_path,
            progress_callback=progress_callback
        )
    else:
        logger.error(f"Unknown transcription engine '{selected_engine}'. Must be 'basic-pitch' or 'muscriptor'.")
        return None


def audio_to_midi(
    audio_path: str,
    output_path: Optional[str] = None,
    engine: Optional[str] = None
) -> Optional[str]:
    """
    Backwards-compatible helper: converts audio file to .mid and returns output file path.
    """
    if output_path is None:
        base, _ = os.path.splitext(audio_path)
        output_path = f"{base}.mid"

    result = transcribe_audio(audio_path=audio_path, output_path=output_path, engine=engine)
    if result and Path(output_path).exists():
        return output_path
    return None
