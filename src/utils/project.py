"""
Kraftbeat Project File Management

Save and load entire session state including prompts, settings, and audio references.
Project files are stored as JSON with .kraftbeat extension.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

PROJECT_VERSION = "1.0"
PROJECT_EXTENSION = ".kraftbeat"


def create_project_data(
    prompt: str = "",
    duration: int = 10,
    temperature: float = 1.0,
    model_name: str = "facebook/musicgen-small",
    bpm_enabled: bool = False,
    bpm: int = 120,
    key_enabled: bool = False,
    key_name: str = "C Major",
    continuation_mode: bool = False,
    seamless_loop: bool = False,
    reverb: int = 0,
    compression: int = 0,
    bass_eq: int = 0,
    treble_eq: int = 0,
    format_type: str = "WAV",
    bitrate: str = "192k",
    notes: str = "",
    audio_files: list = None,
) -> Dict[str, Any]:
    """Create a project data dictionary."""
    return {
        "version": PROJECT_VERSION,
        "created": datetime.now().isoformat(),
        "modified": datetime.now().isoformat(),
        
        # Generation settings
        "prompt": prompt,
        "duration": duration,
        "temperature": temperature,
        "model_name": model_name,
        
        # Music controls
        "bpm_enabled": bpm_enabled,
        "bpm": bpm,
        "key_enabled": key_enabled,
        "key_name": key_name,
        "continuation_mode": continuation_mode,
        "seamless_loop": seamless_loop,
        
        # Effects
        "effects": {
            "reverb": reverb,
            "compression": compression,
            "bass_eq": bass_eq,
            "treble_eq": treble_eq,
        },
        
        # Export settings
        "export": {
            "format": format_type,
            "bitrate": bitrate,
        },
        
        # Metadata
        "notes": notes,
        "audio_files": audio_files or [],  # List of related audio file paths
    }


def save_project(filepath: str, project_data: Dict[str, Any]) -> bool:
    """
    Save project to file.
    
    Args:
        filepath: Path to save project file
        project_data: Project data dictionary
        
    Returns:
        True if successful
    """
    try:
        filepath = Path(filepath)
        if filepath.suffix.lower() != PROJECT_EXTENSION:
            filepath = filepath.with_suffix(PROJECT_EXTENSION)
        
        # Update modified time
        project_data["modified"] = datetime.now().isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2)
        
        logger.info(f"Project saved to: {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save project: {e}")
        return False


def load_project(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Load project from file.
    
    Args:
        filepath: Path to project file
        
    Returns:
        Project data dictionary or None on failure
    """
    try:
        filepath = Path(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        
        # Validate version
        version = project_data.get("version", "0.0")
        if version != PROJECT_VERSION:
            logger.warning(f"Project version mismatch: {version} vs {PROJECT_VERSION}")
        
        logger.info(f"Project loaded from: {filepath}")
        return project_data
        
    except Exception as e:
        logger.error(f"Failed to load project: {e}")
        return None


def get_recent_projects(projects_dir: str, limit: int = 10) -> list:
    """
    Get list of recent project files sorted by modification time.
    
    Args:
        projects_dir: Directory to search for projects
        limit: Maximum number of projects to return
        
    Returns:
        List of (filepath, modified_time) tuples
    """
    try:
        projects_dir = Path(projects_dir)
        if not projects_dir.exists():
            return []
        
        projects = []
        for filepath in projects_dir.glob(f"*{PROJECT_EXTENSION}"):
            try:
                mtime = filepath.stat().st_mtime
                projects.append((str(filepath), mtime))
            except Exception as e:
                logger.debug(f"Failed to get stat for project file {filepath}: {e}")
        
        # Sort by modification time (newest first)
        projects.sort(key=lambda x: x[1], reverse=True)
        return projects[:limit]
        
    except Exception as e:
        logger.error(f"Failed to list projects: {e}")
        return []
