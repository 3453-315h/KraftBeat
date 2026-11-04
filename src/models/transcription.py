"""
Transcription Data Model for Audio-to-MIDI.

Provides a unified representation of musical transcription events, beat grids,
and engine-specific capability flags (velocity, pitch bend) across engines
(Spotify basic-pitch, MuScriptor/NeuralNote).
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any


@dataclass
class TranscriptionNote:
    """Individual transcribed note event."""
    onset_sec: float
    offset_sec: float
    pitch: int  # MIDI pitch 0-127
    instrument: str = "acoustic_grand_piano"
    velocity: Optional[int] = None  # None for engines without dynamics recovery (e.g. MuScriptor)
    pitch_bend: Optional[List[int]] = None  # None for engines without pitch bend recovery


def notes_to_smf_bytes(notes: List[TranscriptionNote], tempo: float = 120.0, default_velocity: int = 100) -> bytes:
    """Generate standard Type 0 MIDI bytes (SMF) from notes without external dependencies."""
    import struct

    def write_varlen(val: int) -> bytes:
        buf = bytearray()
        val = int(max(0, val))
        buf.append(val & 0x7F)
        val >>= 7
        while val > 0:
            buf.insert(0, (val & 0x7F) | 0x80)
            val >>= 7
        return bytes(buf)

    ticks_per_beat = 480
    events = []
    for n in notes:
        t_on = int(n.onset_sec * (tempo / 60.0) * ticks_per_beat)
        t_off = int(n.offset_sec * (tempo / 60.0) * ticks_per_beat)
        if t_off <= t_on:
            t_off = t_on + int(0.1 * (tempo / 60.0) * ticks_per_beat)
        vel = n.velocity if n.velocity is not None else default_velocity
        events.append((t_on, 1, n.pitch, vel))   # 1 = note_on
        events.append((t_off, 0, n.pitch, 0))    # 0 = note_off

    events.sort(key=lambda x: (x[0], x[1]))

    track = bytearray()
    # Tempo meta-event
    mpqn = int(60_000_000 / max(tempo, 1.0))
    track.extend(b"\x00\xFF\x51\x03" + struct.pack(">I", mpqn)[1:])

    last_tick = 0
    for tick, ev_type, pitch, vel in events:
        delta = max(0, tick - last_tick)
        last_tick = tick
        track.extend(write_varlen(delta))
        if ev_type == 1:
            track.extend(b"\x90" + bytes([pitch & 0x7F, vel & 0x7F]))
        else:
            track.extend(b"\x80" + bytes([pitch & 0x7F, 0]))

    # End of track meta-event
    track.extend(b"\x00\xFF\x2F\x00")

    header = b"MThd" + struct.pack(">IHHH", 6, 0, 1, ticks_per_beat)
    track_chunk = b"MTrk" + struct.pack(">I", len(track)) + bytes(track)
    return header + track_chunk


@dataclass
class TranscriptionResult:
    """
    Complete audio transcription output.
    
    Capability flags (has_velocity, has_pitch_bend) explicitly communicate
    whether the source engine extracted continuous dynamics or if constant
    values are used for MIDI serialization.
    """
    notes: List[TranscriptionNote] = field(default_factory=list)
    tempo: float = 120.0
    time_signature: Optional[str] = None
    is_placeholder_grid: bool = False
    duration: float = 0.0
    source_audio_path: str = ""
    engine_id: str = "basic-pitch"  # 'basic-pitch' | 'muscriptor'
    model_size: Optional[str] = None
    has_velocity: bool = False
    has_pitch_bend: bool = False
    midi_bytes: Optional[bytes] = None

    def get_instruments(self) -> List[str]:
        """Return list of distinct instruments present in transcription."""
        seen = set()
        instruments = []
        for n in self.notes:
            if n.instrument not in seen:
                seen.add(n.instrument)
                instruments.append(n.instrument)
        return instruments

    def get_notes_for_instrument(self, instrument: str) -> List[TranscriptionNote]:
        """Return all notes transcribed for a specific instrument."""
        return [n for n in self.notes if n.instrument == instrument]

    def save_midi(self, output_path: str) -> bool:
        """Write serialized MIDI bytes to disk."""
        if not self.midi_bytes and self.notes:
            self.midi_bytes = notes_to_smf_bytes(self.notes, tempo=self.tempo)
        if not self.midi_bytes:
            return False
        try:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(self.midi_bytes)
            return True
        except Exception:
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary representation for IPC or logging."""
        return {
            "engine_id": self.engine_id,
            "model_size": self.model_size,
            "tempo": self.tempo,
            "time_signature": self.time_signature,
            "is_placeholder_grid": self.is_placeholder_grid,
            "duration": self.duration,
            "source_audio_path": self.source_audio_path,
            "has_velocity": self.has_velocity,
            "has_pitch_bend": self.has_pitch_bend,
            "note_count": len(self.notes),
            "instruments": self.get_instruments(),
        }
