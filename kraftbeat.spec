# -*- mode: python ; coding: utf-8 -*-
"""
Kraftbeat PyInstaller Spec File

Build with: pyinstaller kraftbeat.spec
"""

import sys
from pathlib import Path

# Get project root
PROJ_ROOT = Path(SPECPATH)

a = Analysis(
    ['src/ui/main_window.py'],
    pathex=[str(PROJ_ROOT), str(PROJ_ROOT / 'src')],
    binaries=[],
    datas=[
        (str(PROJ_ROOT / 'src' / 'ui' / 'assets' / 'icons'), 'src/ui/assets/icons'),
        (str(PROJ_ROOT / 'config'), 'config'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'numpy',
        'soundfile',
        'sounddevice',
        'pyqtgraph',
        'scipy',
        'scipy.io',
        'scipy.io.wavfile',
        'torch',
        'transformers',
        'torch_directml',
        'fastapi',
        'uvicorn',
        'audiocraft',
        'demucs',
        'basic_pitch',
        'keyring',
        'psutil',
        'PIL',
        'PIL.Image',
        'src.aoide',
        'src.aoide.backend',
        'src.aoide.abc_tools',
        'src.models.yue2',
        'src.models.transcription',
        'src.models.ace_step',
        'src.models.diffrhythm',
        'src.models.musicgen',
        'src.models.catalog',
        'src.ui.panels.transcription_panel',
        'src.ui.panels.aoide_panel',
        'src.ui.panels.arranger_panel',
        'src.ui.panels.stems_panel',
        'src.ui.panels.diffrhythm_panel',
        'src.ui.panels.ace_step_panel',
        'src.utils.midi_muscriptor',
        'src.utils.muscriptor_worker',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'tkinter',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Kraftbeat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if available
)
