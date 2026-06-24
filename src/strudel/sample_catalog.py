"""
Strudel Sample Pack Catalog.

Available sample packs for download to enable offline Strudel functionality.
"""

STRUDEL_SAMPLE_CATALOG = {
    # =====================================================================
    # ESSENTIAL PACKS (Core for most patterns)
    # =====================================================================
    "tidal-drum-machines": {
        "display_name": "Tidal Drum Machines",
        "description": "909, 808, LinnDrum, SP1200, and 40+ classic drum machines",
        "repo": "ritchse/tidal-drum-machines",
        "branch": "main",
        "json_file": "tidal-drum-machines.json",
        "samples_folder": "machines",
        "size_estimate": "~150 MB",
        "category": "Drums",
        "essential": True,
    },
    "dirt-samples": {
        "display_name": "Dirt-Samples",
        "description": "Classic SuperDirt/TidalCycles samples (bd, sd, hh, etc.)",
        "repo": "tidalcycles/Dirt-Samples",
        "branch": "master",
        "json_file": None,  # We generate this
        "samples_folder": ".",
        "size_estimate": "~500 MB",
        "category": "Drums",
        "essential": True,
    },
    # =====================================================================
    # INSTRUMENTS
    # =====================================================================
    "piano": {
        "display_name": "Salamander Piano",
        "description": "High quality grand piano samples",
        "repo": "felixroos/dough-samples",
        "branch": "main",
        "subpath": "piano",
        "json_file": "piano.json",
        "size_estimate": "~60 MB",
        "category": "Instruments",
        "essential": False,
    },
    "vcsl": {
        "display_name": "VCSL Orchestra",
        "description": "Versilian Community Sample Library - orchestral instruments",
        "repo": "felixroos/VCSL",
        "branch": "master",
        "json_file": "vcsl.json",
        "size_estimate": "~200 MB",
        "category": "Instruments",
        "essential": False,
    },
    # =====================================================================
    # WORLD / PERCUSSION
    # =====================================================================
    "mridangam": {
        "display_name": "Mridangam",
        "description": "South Indian percussion samples",
        "repo": "yaxu/mrid",
        "branch": "main",
        "json_file": "mridangam.json",
        "size_estimate": "~10 MB",
        "category": "World",
        "essential": False,
    },
    "capoeira": {
        "display_name": "Capoeira",
        "description": "Brazilian capoeira percussion and voice samples",
        "repo": "salsicha/capoeira_strudel",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~20 MB",
        "category": "World",
        "essential": False,
    },
    "rochormatic": {
        "display_name": "Rochormatic",
        "description": "Singapore/world music samples collection",
        "repo": "sonidosingapura/rochormatic",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~30 MB",
        "category": "World",
        "essential": False,
    },
    "dough-juj": {
        "display_name": "Dough-Juj",
        "description": "World music and ethnic percussion samples",
        "repo": "Bubobubobubobubo/Dough-Juj",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~25 MB",
        "category": "World",
        "essential": False,
    },
    # =====================================================================
    # ELECTRONIC / SYNTH
    # =====================================================================
    "dough-fox": {
        "display_name": "Dough-Fox",
        "description": "Foxy samples collection by Bubobubobubobubo",
        "repo": "Bubobubobubobubo/Dough-Fox",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~50 MB",
        "category": "Electronic",
        "essential": False,
    },
    "mirus": {
        "display_name": "Mirus",
        "description": "Electronic and experimental samples",
        "repo": "TristanCacqueray/mirus",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~40 MB",
        "category": "Electronic",
        "essential": False,
    },
    "quantum-music": {
        "display_name": "Quantum Music",
        "description": "Experimental quantum-inspired sounds",
        "repo": "QuantumVillage/quantum-music",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~15 MB",
        "category": "Experimental",
        "essential": False,
    },
    "todepond": {
        "display_name": "TodePond Samples",
        "description": "Experimental and creative samples",
        "repo": "TodePond/samples",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~20 MB",
        "category": "Experimental",
        "essential": False,
    },
    # =====================================================================
    # BREAKS / JUNGLE
    # =====================================================================
    "dough-amen": {
        "display_name": "Dough-Amen",
        "description": "Amen break and jungle samples",
        "repo": "Bubobubobubobubo/Dough-Amen",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~30 MB",
        "category": "Breaks",
        "essential": False,
    },
    "clean-breaks": {
        "display_name": "Clean Breaks",
        "description": "Clean breakbeat samples by yaxu",
        "repo": "yaxu/clean-breaks",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~20 MB",
        "category": "Breaks",
        "essential": False,
    },
    "spicule": {
        "display_name": "Spicule",
        "description": "Experimental breaks and textures",
        "repo": "yaxu/spicule",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~30 MB",
        "category": "Breaks",
        "essential": False,
    },
    # =====================================================================
    # RETRO / CHIPTUNE
    # =====================================================================
    "dough-amiga": {
        "display_name": "Dough-Amiga",
        "description": "Classic Amiga/MOD tracker samples",
        "repo": "Bubobubobubobubo/Dough-Amiga",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~40 MB",
        "category": "Retro",
        "essential": False,
    },
    # =====================================================================
    # DJ / VINYL
    # =====================================================================
    "crate": {
        "display_name": "Crate",
        "description": "DJ and vinyl samples, scratches, loops",
        "repo": "eddyflux/crate",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~100 MB",
        "category": "DJ",
        "essential": False,
    },
    # =====================================================================
    # AMBIENT / FIELD RECORDINGS
    # =====================================================================
    "departure": {
        "display_name": "Departure",
        "description": "Ambient textures and atmospheric sounds",
        "repo": "prismograph/departure",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~40 MB",
        "category": "Ambient",
        "essential": False,
    },
    "garden": {
        "display_name": "Garden",
        "description": "Nature and field recording samples",
        "repo": "mot4i/garden",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~25 MB",
        "category": "Ambient",
        "essential": False,
    },
    # =====================================================================
    # MIXED / GENERAL
    # =====================================================================
    "algorave-dave": {
        "display_name": "Algorave Dave",
        "description": "Mixed samples from Algorave community",
        "repo": "algorave-dave/samples",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~50 MB",
        "category": "Mixed",
        "essential": False,
    },
    "livecoding-samples": {
        "display_name": "Livecoding Samples",
        "description": "General purpose livecoding sample collection",
        "repo": "wyan/livecoding-samples",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~35 MB",
        "category": "Mixed",
        "essential": False,
    },
    "strudel-songs": {
        "display_name": "Strudel Songs",
        "description": "Example song patterns and samples",
        "repo": "eefano/strudel-songs-collection",
        "branch": "main",
        "json_file": "strudel.json",
        "size_estimate": "~45 MB",
        "category": "Mixed",
        "essential": False,
    },
}

# Categories for UI grouping
SAMPLE_CATEGORIES = [
    "Drums",
    "Instruments",
    "World",
    "Electronic",
    "Experimental",
    "Breaks",
    "Retro",
    "DJ",
    "Ambient",
    "Mixed",
]
