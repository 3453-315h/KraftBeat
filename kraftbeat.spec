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
    pathex=[str(PROJ_ROOT / 'src')],
    binaries=[],
    datas=[
        # Include any data files if needed
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'numpy',
        'sounddevice',
        'pyqtgraph',
        'scipy',
        'scipy.io',
        'scipy.io.wavfile',
        'torch',
        'transformers',
        'torch_directml',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'tkinter',
        'PIL',
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
