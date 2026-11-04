#!/usr/bin/env bash
set -e

# Kraftbeat - Linux Launcher
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "   Kraftbeat - AI Music Generator       "
echo "========================================"

# Activate existing virtual environment if present
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the application
echo "Starting Kraftbeat UI..."
python3 -m src.ui.main_window "$@"

