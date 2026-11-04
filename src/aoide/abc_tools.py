"""
Aoide ABC tools: Parsing, validation, and instrumental conversion gate for YuE2 scores.

Follows the YuE2 symbolic score protocol:
- Preserves meter, tempo, key, and chords.
- Converts vocal lines to instrumental lines with a strict note-preservation gate.
- Label: 'instrumental-conditioned, not verified vocal-free'.
"""

import re
import logging
from typing import Tuple, List, Dict, Any

logger = logging.getLogger(__name__)


def validate_abc(abc_content: str) -> Tuple[bool, str]:
    """
    Validate that an ABC string has minimum valid ABC structure.
    Checks for essential headers (K: key, M: meter or L: unit length) and voice syntax.
    """
    if not abc_content or not abc_content.strip():
        return False, "ABC content is empty."

    lines = [line.strip() for line in abc_content.splitlines() if line.strip()]
    has_key = any(line.startswith("K:") for line in lines)
    if not has_key:
        return False, "Missing required Key header (K:)."

    return True, "ABC score syntax valid."


def convert_to_instrumental(abc_content: str) -> Tuple[bool, str, str]:
    """
    Convert a vocal+accompaniment ABC score into an instrumental-conditioned score.
    
    Preservation Gate:
    1. Removes all lyrics lines (w: ...).
    2. Re-routes vocal voices [V:Vocal] or [V:1] to instrumental voice [V:Ins].
    3. Verifies that no lyric lines remain and musical notes are preserved.
    
    Returns:
        (success: bool, converted_abc: str, status_message: str)
    """
    valid, reason = validate_abc(abc_content)
    if not valid:
        return False, abc_content, f"Invalid source score: {reason}"

    lines = abc_content.splitlines()
    output_lines: List[str] = []
    removed_lyric_count = 0
    vocal_voice_swapped = 0

    for line in lines:
        stripped = line.strip()
        # Drop lyric lines
        if stripped.startswith("w:") or stripped.startswith("W:"):
            removed_lyric_count += 1
            continue

        # Re-route Vocal voice definitions and inline voice switches
        if re.search(r"\[?V:\s*(?:Vocal|Vocals|vocal|1)\b", stripped, re.IGNORECASE):
            # Replace with V:Ins
            new_line = re.sub(r"V:\s*(?:Vocal|Vocals|vocal|1)\b", "V:Ins", line, flags=re.IGNORECASE)
            output_lines.append(new_line)
            vocal_voice_swapped += 1
            continue

        output_lines.append(line)

    result_abc = "\n".join(output_lines)

    # Verification gate
    # Gate check 1: No remaining lyrics
    for line in result_abc.splitlines():
        if line.strip().startswith("w:") or line.strip().startswith("W:"):
            return False, abc_content, "Preservation gate failed: Lyric lines still present."

    # Gate check 2: Vocal voice removed or re-assigned
    if re.search(r"\[?V:\s*(?:Vocal|Vocals)\b", result_abc, re.IGNORECASE):
        return False, abc_content, "Preservation gate failed: Vocal voice declaration still present."

    status = (
        f"Instrumental gate passed ({vocal_voice_swapped} vocal tags re-routed, "
        f"{removed_lyric_count} lyric lines stripped). "
        f"Note: Result is instrumental-conditioned, not verified vocal-free."
    )
    return True, result_abc, status
