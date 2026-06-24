"""
Kraftbeat Audio-to-MIDI Utilities

Extracts polyphonic MIDI from audio stems using Spotify's basic-pitch.
"""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

def audio_to_midi(audio_path: str, output_path: Optional[str] = None) -> Optional[str]:
    """
    Convert an audio file to a MIDI file using basic-pitch.
    
    Args:
        audio_path: Path to the input audio file (.wav, .mp3, etc.)
        output_path: Optional path for the output .mid file. If None, it will be saved next to the input.
        
    Returns:
        The path to the generated .mid file, or None if conversion failed.
    """
    try:
        from basic_pitch.inference import predict_and_save
        from basic_pitch import ICASSP_2022_MODEL_PATH
        
        if output_path is None:
            base, _ = os.path.splitext(audio_path)
            output_path = f"{base}.mid"
            
        output_dir = os.path.dirname(os.path.abspath(output_path))
        
        logger.info(f"Extracting MIDI from {audio_path}...")
        
        # predict_and_save takes (audio_path_list, output_directory, save_midi, sonify_midi, save_model_outputs, save_notes)
        predict_and_save(
            [audio_path],
            output_dir,
            save_midi=True,
            sonify_midi=False,
            save_model_outputs=False,
            save_notes=False
        )
        
        # predict_and_save saves the file as "filename_basic_pitch.mid" by default.
        # Let's rename it to the requested output_path.
        base_name = os.path.basename(audio_path)
        name_no_ext, _ = os.path.splitext(base_name)
        default_midi_path = os.path.join(output_dir, f"{name_no_ext}_basic_pitch.mid")
        
        if os.path.exists(default_midi_path):
            if default_midi_path != output_path:
                # If target already exists, remove it
                if os.path.exists(output_path):
                    os.remove(output_path)
                os.rename(default_midi_path, output_path)
            logger.info(f"MIDI extracted successfully: {output_path}")
            return output_path
        else:
            logger.error("basic-pitch did not generate a MIDI file.")
            return None
            
    except ImportError:
        logger.error("basic-pitch is not installed. Please run: pip install basic-pitch")
        return None
    except Exception as e:
        logger.error(f"Failed to extract MIDI: {e}")
        import traceback
        traceback.print_exc()
        return None
