#!/usr/bin/env bash
set -e

# Kraftbeat - Linux Build Script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "   Kraftbeat Linux Build Script         "
echo "========================================"

if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found in active PATH."
    echo "Please install PyInstaller (e.g., 'pip install pyinstaller' or 'uv pip install pyinstaller')."
    exit 1
fi

echo "Building Kraftbeat binary using kraftbeat.spec..."
pyinstaller kraftbeat.spec --noconfirm

echo "========================================"
if [ -f "dist/Kraftbeat" ]; then
    echo "BUILD SUCCESSFUL!"
    echo "Output: dist/Kraftbeat"
else
    echo "BUILD FAILED!"
fi
echo "========================================"

