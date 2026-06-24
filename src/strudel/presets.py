"""
Strudel Pattern Preset Loader.

Loads and manages JavaScript pattern presets organized by genre.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Path to presets folder (src/strudel/presets.py → src/strudel → src → kraftbeat)
PRESETS_PATH = Path(__file__).parent.parent.parent / "strudel_presets"

# Genre categories
PRESET_GENRES = [
    "techno",
    "house",
    "drum_and_bass",
    "hip_hop",
    "ambient",
    "world",
    "experimental",
    "dubstep",
    "classic",
    "lofi",
]


def get_presets_by_genre() -> Dict[str, List[Dict]]:
    """
    Load all presets organized by genre.
    
    Returns:
        Dict mapping genre name to list of preset info dicts.
    """
    presets = {}
    
    for genre in PRESET_GENRES:
        genre_path = PRESETS_PATH / genre
        if genre_path.exists():
            genre_presets = []
            for preset_file in sorted(genre_path.glob("*.js")):
                preset_info = parse_preset_file(preset_file)
                if preset_info:
                    genre_presets.append(preset_info)
            if genre_presets:
                presets[genre] = genre_presets
    
    return presets


def parse_preset_file(file_path: Path) -> Optional[Dict]:
    """
    Parse a preset file and extract metadata from comments.
    
    Expected format:
        // @name Four on Floor
        // @genre Techno
        // @bpm 130
        // @tags kick, minimal, driving
        
        <pattern code>
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        
        # Parse metadata from comments
        metadata = {
            "file": file_path.name,
            "path": str(file_path),
            "code": content,
        }
        
        for line in content.split("\n")[:20]:  # Check first 20 lines
            line = line.strip()
            if line.startswith("// @"):
                parts = line[4:].split(" ", 1)
                if len(parts) == 2:
                    key, value = parts
                    metadata[key.lower()] = value.strip()
        
        # Ensure required fields
        if "name" not in metadata:
            metadata["name"] = file_path.stem.replace("_", " ").title()
        
        return metadata
    except Exception as e:
        logger.error(f"Error parsing preset {file_path}: {e}")
        return None


def get_preset_code(genre: str, preset_name: str) -> Optional[str]:
    """
    Get the code for a specific preset.
    
    Args:
        genre: Genre folder name
        preset_name: Preset filename (without .js)
    
    Returns:
        JavaScript code or None if not found.
    """
    preset_path = PRESETS_PATH / genre / f"{preset_name}.js"
    if preset_path.exists():
        return preset_path.read_text(encoding="utf-8")
    return None


def list_all_presets() -> List[Dict]:
    """
    Get a flat list of all available presets.
    
    Returns:
        List of preset info dicts with genre included.
    """
    all_presets = []
    presets_by_genre = get_presets_by_genre()
    
    for genre, presets in presets_by_genre.items():
        for preset in presets:
            preset["genre"] = genre
            all_presets.append(preset)
    
    return all_presets


# Preset catalog for UI display (summary without full code)
PRESET_CATALOG = {
    "techno": [
        {"name": "Four on Floor", "bpm": 130, "tags": "kick, minimal, driving"},
        {"name": "Acid Bassline", "bpm": 135, "tags": "303, squelchy, hypnotic"},
        {"name": "Berlin Minimal", "bpm": 128, "tags": "sparse, deep, clicking"},
    ],
    "house": [
        {"name": "Chicago Classic", "bpm": 122, "tags": "piano, chords, soulful"},
        {"name": "Deep Groove", "bpm": 120, "tags": "bass, warm, groove"},
        {"name": "Disco Filter", "bpm": 118, "tags": "filter, funky, uplifting"},
    ],
    "drum_and_bass": [
        {"name": "Amen Chop", "bpm": 174, "tags": "break, jungle, chopped"},
        {"name": "Liquid Drums", "bpm": 170, "tags": "smooth, rolling, melodic"},
        {"name": "Neurofunk Bass", "bpm": 176, "tags": "dark, aggressive, wobble"},
    ],
    "hip_hop": [
        {"name": "Boom Bap", "bpm": 90, "tags": "classic, vinyl, drums"},
        {"name": "Lo-Fi Chill", "bpm": 85, "tags": "dusty, relaxing, jazz"},
        {"name": "Trap Hats", "bpm": 140, "tags": "808, rolling, hard"},
    ],
    "ambient": [
        {"name": "Drone Pad", "bpm": 60, "tags": "slow, evolving, peaceful"},
        {"name": "Generative Melody", "bpm": 80, "tags": "random, evolving, notes"},
        {"name": "Granular Texture", "bpm": 70, "tags": "grains, atmospheric, subtle"},
    ],
    "world": [
        {"name": "Afrobeat", "bpm": 110, "tags": "percussion, polyrhythm, groovy"},
        {"name": "Indian Tabla", "bpm": 100, "tags": "tabla, mridangam, rhythm"},
        {"name": "Gamelan", "bpm": 90, "tags": "metallic, hypnotic, layered"},
    ],
    "experimental": [
        {"name": "Euclidean Rhythms", "bpm": 120, "tags": "mathematical, complex, shifting"},
        {"name": "Polymetric Layers", "bpm": 110, "tags": "multiple, time, signatures"},
        {"name": "Probability Drums", "bpm": 130, "tags": "random, weighted, evolving"},
    ],
    "classic": [
        {"name": "Jazz Swing", "bpm": 130, "tags": "swing, jazzy, brushes"},
        {"name": "Funk Groove", "bpm": 105, "tags": "funky, groovy, bass"},
    ],
    "dubstep": [
        {"name": "Wobble Bass", "bpm": 140, "tags": "wobble, heavy, bass"},
        {"name": "Riddim", "bpm": 150, "tags": "heavy, riddim, aggressive"},
    ],
}

