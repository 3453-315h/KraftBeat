"""
Strudel Visual Themes.

CSS themes for customizing the Strudel live coding environment.
"""

from pathlib import Path

# Path to themes folder (src/strudel/themes.py → src/strudel → src → kraftbeat)
THEMES_PATH = Path(__file__).parent.parent.parent / "strudel_themes"

# Available themes with their color schemes
STRUDEL_THEMES = {
    "kraftbeat": {
        "display_name": "Kraftbeat",
        "description": "Match app dark theme",
        "colors": {
            "background": "#1a1a22",
            "editor_bg": "#252530",
            "accent": "#648cff",
            "text": "#e0e0e0",
            "highlight": "#4a5568",
        },
        "css": """
            body { background: #1a1a22 !important; }
            .cm-editor { background: #252530 !important; }
            .cm-gutters { background: #1e1e28 !important; border-right: 1px solid #404050 !important; }
            .cm-activeLineGutter { background: #2a2a38 !important; }
            .cm-activeLine { background: #2a2a38 !important; }
            .cm-cursor { border-left-color: #648cff !important; }
            .cm-selectionBackground { background: #3a4a6a !important; }
            header { background: #1a1a22 !important; border-bottom: 1px solid #404050 !important; }
            button { background: #2a2a38 !important; border: 1px solid #404050 !important; }
            button:hover { background: #3a3a48 !important; }
        """,
    },
    "neon_nights": {
        "display_name": "Neon Nights",
        "description": "Cyberpunk purple/pink",
        "colors": {
            "background": "#0d0d1a",
            "editor_bg": "#1a1a2e",
            "accent": "#9945FF",
            "text": "#e0e0e0",
            "highlight": "#FF45E3",
        },
        "css": """
            body { background: #0d0d1a !important; }
            .cm-editor { background: #1a1a2e !important; }
            .cm-gutters { background: #12121f !important; border-right: 1px solid #9945FF40 !important; }
            .cm-activeLineGutter { background: #251a35 !important; }
            .cm-activeLine { background: #251a3540 !important; }
            .cm-cursor { border-left-color: #FF45E3 !important; }
            .cm-selectionBackground { background: #9945FF40 !important; }
            header { background: linear-gradient(90deg, #0d0d1a, #1a0d2a) !important; }
            button { background: #2a1a4a !important; border: 1px solid #9945FF80 !important; }
            button:hover { background: #3a2a5a !important; box-shadow: 0 0 10px #9945FF40 !important; }
        """,
    },
    "forest": {
        "display_name": "Forest",
        "description": "Dark green/brown",
        "colors": {
            "background": "#0d1a0d",
            "editor_bg": "#1a2a1a",
            "accent": "#2D5A27",
            "text": "#c0d0c0",
            "highlight": "#8B4513",
        },
        "css": """
            body { background: #0d1a0d !important; }
            .cm-editor { background: #1a2a1a !important; }
            .cm-gutters { background: #12201a !important; border-right: 1px solid #2D5A2780 !important; }
            .cm-activeLineGutter { background: #1a351a !important; }
            .cm-activeLine { background: #1a351a40 !important; }
            .cm-cursor { border-left-color: #8B4513 !important; }
            .cm-selectionBackground { background: #2D5A2740 !important; }
            header { background: #0d1a0d !important; }
            button { background: #1a351a !important; border: 1px solid #2D5A2780 !important; }
        """,
    },
    "ocean": {
        "display_name": "Ocean",
        "description": "Deep blue/cyan",
        "colors": {
            "background": "#0a1520",
            "editor_bg": "#0d2030",
            "accent": "#0077B6",
            "text": "#c0e0f0",
            "highlight": "#00D4FF",
        },
        "css": """
            body { background: #0a1520 !important; }
            .cm-editor { background: #0d2030 !important; }
            .cm-gutters { background: #0a1825 !important; border-right: 1px solid #0077B680 !important; }
            .cm-activeLineGutter { background: #102540 !important; }
            .cm-activeLine { background: #10254040 !important; }
            .cm-cursor { border-left-color: #00D4FF !important; }
            .cm-selectionBackground { background: #0077B640 !important; }
            header { background: linear-gradient(90deg, #0a1520, #0d2030) !important; }
            button { background: #0d2535 !important; border: 1px solid #0077B680 !important; }
        """,
    },
    "fire": {
        "display_name": "Fire",
        "description": "Red/orange",
        "colors": {
            "background": "#1a0d0d",
            "editor_bg": "#2a1515",
            "accent": "#FF4500",
            "text": "#f0d0c0",
            "highlight": "#FFD700",
        },
        "css": """
            body { background: #1a0d0d !important; }
            .cm-editor { background: #2a1515 !important; }
            .cm-gutters { background: #20100a !important; border-right: 1px solid #FF450080 !important; }
            .cm-activeLineGutter { background: #351a1a !important; }
            .cm-activeLine { background: #351a1a40 !important; }
            .cm-cursor { border-left-color: #FFD700 !important; }
            .cm-selectionBackground { background: #FF450040 !important; }
            header { background: linear-gradient(90deg, #1a0d0d, #2a1010) !important; }
            button { background: #351a15 !important; border: 1px solid #FF450080 !important; }
        """,
    },
    "midnight": {
        "display_name": "Midnight",
        "description": "Pure dark minimal",
        "colors": {
            "background": "#0D0D0D",
            "editor_bg": "#121212",
            "accent": "#3a3a4a",
            "text": "#a0a0a0",
            "highlight": "#505060",
        },
        "css": """
            body { background: #0D0D0D !important; }
            .cm-editor { background: #121212 !important; }
            .cm-gutters { background: #0a0a0a !important; border-right: 1px solid #2a2a3a !important; }
            .cm-activeLineGutter { background: #181818 !important; }
            .cm-activeLine { background: #18181840 !important; }
            .cm-cursor { border-left-color: #808090 !important; }
            .cm-selectionBackground { background: #3a3a4a40 !important; }
            header { background: #0D0D0D !important; border-bottom: 1px solid #1a1a2a !important; }
            button { background: #1a1a1a !important; border: 1px solid #2a2a3a !important; }
        """,
    },
    "sunrise": {
        "display_name": "Sunrise",
        "description": "Warm orange/yellow",
        "colors": {
            "background": "#1a1510",
            "editor_bg": "#2a2015",
            "accent": "#FF6B35",
            "text": "#f0e0d0",
            "highlight": "#F7B733",
        },
        "css": """
            body { background: #1a1510 !important; }
            .cm-editor { background: #2a2015 !important; }
            .cm-gutters { background: #1f1810 !important; border-right: 1px solid #FF6B3580 !important; }
            .cm-activeLineGutter { background: #352a1a !important; }
            .cm-activeLine { background: #352a1a40 !important; }
            .cm-cursor { border-left-color: #F7B733 !important; }
            .cm-selectionBackground { background: #FF6B3540 !important; }
            header { background: linear-gradient(90deg, #1a1510, #2a1a10) !important; }
            button { background: #352515 !important; border: 1px solid #FF6B3580 !important; }
        """,
    },
    "arctic": {
        "display_name": "Arctic",
        "description": "Ice blue/white",
        "colors": {
            "background": "#0f1520",
            "editor_bg": "#1a2535",
            "accent": "#A8D8EA",
            "text": "#e8f4f8",
            "highlight": "#FFFFFF",
        },
        "css": """
            body { background: #0f1520 !important; }
            .cm-editor { background: #1a2535 !important; }
            .cm-gutters { background: #121c28 !important; border-right: 1px solid #A8D8EA60 !important; }
            .cm-activeLineGutter { background: #1f3045 !important; }
            .cm-activeLine { background: #1f304540 !important; }
            .cm-cursor { border-left-color: #FFFFFF !important; }
            .cm-selectionBackground { background: #A8D8EA40 !important; }
            header { background: linear-gradient(90deg, #0f1520, #152030) !important; }
            button { background: #1f2a3a !important; border: 1px solid #A8D8EA60 !important; }
        """,
    },
    "synthwave": {
        "display_name": "Synthwave",
        "description": "Retro 80s vibes",
        "colors": {
            "background": "#1a0a2e",
            "editor_bg": "#2d1b4e",
            "accent": "#FF00FF",
            "text": "#00FFFF",
            "highlight": "#FF6EC7",
        },
        "css": """
            body { background: linear-gradient(180deg, #1a0a2e, #2d1b4e) !important; }
            .cm-editor { background: #2d1b4e !important; }
            .cm-gutters { background: #1a0a2e !important; border-right: 1px solid #FF00FF60 !important; }
            .cm-activeLineGutter { background: #3d2b5e !important; }
            .cm-activeLine { background: #3d2b5e40 !important; }
            .cm-cursor { border-left-color: #00FFFF !important; }
            .cm-selectionBackground { background: #FF00FF40 !important; }
            header { background: linear-gradient(90deg, #1a0a2e, #2d1b4e) !important; }
            button { background: #3d2b5e !important; border: 1px solid #FF00FF80 !important; color: #00FFFF !important; }
            button:hover { box-shadow: 0 0 15px #FF00FF60 !important; }
        """,
    },
    "matrix": {
        "display_name": "Matrix",
        "description": "Green terminal",
        "colors": {
            "background": "#000000",
            "editor_bg": "#0a0a0a",
            "accent": "#00FF00",
            "text": "#00FF00",
            "highlight": "#003300",
        },
        "css": """
            body { background: #000000 !important; }
            .cm-editor { background: #0a0a0a !important; }
            .cm-gutters { background: #000000 !important; border-right: 1px solid #00FF0040 !important; }
            .cm-activeLineGutter { background: #0a1a0a !important; }
            .cm-activeLine { background: #0a1a0a40 !important; }
            .cm-cursor { border-left-color: #00FF00 !important; }
            .cm-selectionBackground { background: #00330080 !important; }
            .cm-content { color: #00FF00 !important; }
            header { background: #000000 !important; border-bottom: 1px solid #00FF0040 !important; }
            button { background: #001100 !important; border: 1px solid #00FF0060 !important; color: #00FF00 !important; }
        """,
    },
    "vapor": {
        "display_name": "Vaporwave",
        "description": "Aesthetic pink/cyan",
        "colors": {
            "background": "#1a1a2e",
            "editor_bg": "#16213e",
            "accent": "#FF71CE",
            "text": "#01CDFE",
            "highlight": "#B967FF",
        },
        "css": """
            body { background: linear-gradient(135deg, #1a1a2e, #16213e) !important; }
            .cm-editor { background: #16213e !important; }
            .cm-gutters { background: #1a1a2e !important; border-right: 1px solid #FF71CE60 !important; }
            .cm-activeLineGutter { background: #1f2b4e !important; }
            .cm-activeLine { background: #1f2b4e40 !important; }
            .cm-cursor { border-left-color: #01CDFE !important; }
            .cm-selectionBackground { background: #B967FF40 !important; }
            header { background: linear-gradient(90deg, #1a1a2e, #16213e) !important; }
            button { background: #1f2b4e !important; border: 1px solid #FF71CE80 !important; }
            button:hover { box-shadow: 0 0 10px #B967FF60 !important; }
        """,
    },
    "lavender": {
        "display_name": "Lavender",
        "description": "Soft purple/grey",
        "colors": {
            "background": "#1a1520",
            "editor_bg": "#252030",
            "accent": "#9B8AA5",
            "text": "#E0D8E8",
            "highlight": "#6B5B7A",
        },
        "css": """
            body { background: #1a1520 !important; }
            .cm-editor { background: #252030 !important; }
            .cm-gutters { background: #1f1a28 !important; border-right: 1px solid #9B8AA560 !important; }
            .cm-activeLineGutter { background: #302a40 !important; }
            .cm-activeLine { background: #302a4040 !important; }
            .cm-cursor { border-left-color: #E0D8E8 !important; }
            .cm-selectionBackground { background: #6B5B7A40 !important; }
            header { background: #1a1520 !important; }
            button { background: #302a40 !important; border: 1px solid #9B8AA580 !important; }
        """,
    },
    "copper": {
        "display_name": "Copper",
        "description": "Warm metallic",
        "colors": {
            "background": "#1a1512",
            "editor_bg": "#2a2018",
            "accent": "#B87333",
            "text": "#E8D5C4",
            "highlight": "#CD7F32",
        },
        "css": """
            body { background: #1a1512 !important; }
            .cm-editor { background: #2a2018 !important; }
            .cm-gutters { background: #1f1a15 !important; border-right: 1px solid #B8733360 !important; }
            .cm-activeLineGutter { background: #352a20 !important; }
            .cm-activeLine { background: #352a2040 !important; }
            .cm-cursor { border-left-color: #CD7F32 !important; }
            .cm-selectionBackground { background: #B8733340 !important; }
            header { background: linear-gradient(90deg, #1a1512, #2a2018) !important; }
            button { background: #352a20 !important; border: 1px solid #B8733380 !important; }
        """,
    },
    "monochrome": {
        "display_name": "Monochrome",
        "description": "Pure black/white",
        "colors": {
            "background": "#0a0a0a",
            "editor_bg": "#141414",
            "accent": "#808080",
            "text": "#FFFFFF",
            "highlight": "#404040",
        },
        "css": """
            body { background: #0a0a0a !important; }
            .cm-editor { background: #141414 !important; }
            .cm-gutters { background: #0a0a0a !important; border-right: 1px solid #40404080 !important; }
            .cm-activeLineGutter { background: #1e1e1e !important; }
            .cm-activeLine { background: #1e1e1e40 !important; }
            .cm-cursor { border-left-color: #FFFFFF !important; }
            .cm-selectionBackground { background: #40404080 !important; }
            header { background: #0a0a0a !important; border-bottom: 1px solid #404040 !important; }
            button { background: #1e1e1e !important; border: 1px solid #60606080 !important; }
        """,
    },
    "toxic": {
        "display_name": "Toxic",
        "description": "Radioactive green",
        "colors": {
            "background": "#0a0f0a",
            "editor_bg": "#101810",
            "accent": "#39FF14",
            "text": "#CCFF00",
            "highlight": "#00FF00",
        },
        "css": """
            body { background: #0a0f0a !important; }
            .cm-editor { background: #101810 !important; }
            .cm-gutters { background: #080d08 !important; border-right: 1px solid #39FF1460 !important; }
            .cm-activeLineGutter { background: #152215 !important; }
            .cm-activeLine { background: #15221540 !important; }
            .cm-cursor { border-left-color: #CCFF00 !important; }
            .cm-selectionBackground { background: #39FF1440 !important; }
            header { background: linear-gradient(90deg, #0a0f0a, #101810) !important; }
            button { background: #152215 !important; border: 1px solid #39FF1480 !important; }
            button:hover { box-shadow: 0 0 10px #39FF1460 !important; }
        """,
    },
    "sakura": {
        "display_name": "Sakura",
        "description": "Cherry blossom pink",
        "colors": {
            "background": "#1a1218",
            "editor_bg": "#251a22",
            "accent": "#FFB7C5",
            "text": "#F8E8EC",
            "highlight": "#E75480",
        },
        "css": """
            body { background: #1a1218 !important; }
            .cm-editor { background: #251a22 !important; }
            .cm-gutters { background: #1f151c !important; border-right: 1px solid #FFB7C560 !important; }
            .cm-activeLineGutter { background: #302530 !important; }
            .cm-activeLine { background: #30253040 !important; }
            .cm-cursor { border-left-color: #E75480 !important; }
            .cm-selectionBackground { background: #FFB7C540 !important; }
            header { background: #1a1218 !important; }
            button { background: #302530 !important; border: 1px solid #FFB7C580 !important; }
        """,
    },
}


def get_theme_css(theme_id: str) -> str:
    """Get the CSS for a specific theme."""
    if theme_id in STRUDEL_THEMES:
        return STRUDEL_THEMES[theme_id]["css"]
    return STRUDEL_THEMES["kraftbeat"]["css"]


def get_theme_names() -> list:
    """Get list of available theme names for UI dropdown."""
    return [(k, v["display_name"]) for k, v in STRUDEL_THEMES.items()]
