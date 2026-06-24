# Kraftbeat: AI Text-to-Music Generator (Cross-Platform Edition)

GPU-accelerated music generation app supporting **all major hardware backends** — built and tested primarily on DirectML (AMD/Intel Windows).

---

## 1. Supported Backends

| Backend | Hardware | OS | Priority |
|---------|----------|-----|----------|
| **DirectML** | AMD/Intel GPUs | Windows | 🔧 **Primary Dev/Test** |
| **CUDA** | NVIDIA GPUs | Windows/Linux | Production |
| **ROCm** | AMD GPUs | Linux | Production |
| **MPS** | Apple Silicon | macOS | Production |
| **CPU** | Any | All | Fallback |

### Auto-Detection Logic

```python
def get_device():
    if torch.cuda.is_available():
        return "cuda"
    try:
        import torch_directml
        return torch_directml.device()
    except ImportError:
        pass
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"
```

---

## 2. AI Models

### MusicGen (Meta AudioCraft)

| Model | Params | Size | VRAM | Use Case |
|-------|--------|------|------|----------|
| **Small** | 300M | ~1.5 GB | 4 GB | Fast prototyping |
| **Medium** | 1.5B | ~6 GB | 8 GB | Balanced quality/speed |
| **Melody** | 1.5B | ~6 GB | 8 GB | Audio input + text control |
| **Large** | 3.3B | ~12 GB | 16 GB | Maximum fidelity |
| **Stereo** | Various | +overhead | +2-4 GB | Native stereo output |

### Stable Audio Open (Stability AI)

| Model | Params | Size | VRAM | Use Case |
|-------|--------|------|------|----------|
| **1.0** | ~1B | ~4-5 GB | 8-10 GB | Sound FX, loops, ambient |

---

## 3. Requirements

### Core

- **Python 3.10+**
- **FFmpeg** (audio processing)
- **PyTorch** (backend-specific install)

### Backend-Specific PyTorch Install

```bash
# DirectML (Primary - AMD/Intel Windows)
pip install torch-directml

# CUDA (NVIDIA)
pip install torch --index-url https://download.pytorch.org/whl/cu121

# ROCm (AMD Linux)
pip install torch --index-url https://download.pytorch.org/whl/rocm5.6

# CPU Only
pip install torch
```

### Python Libraries

- `transformers` — Model loading
- `accelerate` — VRAM optimization (offload, 8-bit)
- `audiocraft` — MusicGen
- `diffusers` — Stable Audio
- `PyQt6` or `PySide6` — Native window UI
- `pyqtgraph` — Waveform visualization (optional)

---

## 4. Hardware Guidelines

| Tier | GPU | VRAM | Models Supported |
|------|-----|------|------------------|
| Minimum | RX 6500 / GTX 1650 | 4 GB | Small only |
| Recommended | RX 6600 / RTX 3060 | 8-12 GB | Medium, Melody |
| Optimal | RX 7800 / RTX 4070 | 16 GB+ | All models |

---

## 5. Project Structure (Implemented)

```text
kraftbeat/
├── src/
│   ├── device.py           # Backend detection (DirectML/CUDA/MPS)
│   ├── models/
│   │   └── musicgen.py     # MusicGen wrapper
│   ├── ui/
│   │   ├── main_window.py  # PyQt6 main app (~1800 lines)
│   │   ├── workers.py      # Background threads (78 lines)
│   │   ├── themes.py       # Dark/Light styling (350 lines)
│   │   └── panels/
│   │       └── stems_panel.py  # Multi-track stems (280 lines)
│   └── utils/
│       ├── audio.py        # Audio I/O, MP3/FLAC/OGG export
│       ├── effects.py      # Reverb, Compression, EQ (260 lines)
│       └── project.py      # Session save/load (160 lines)
├── outputs/                # Generated audio files
├── run.bat                 # Windows launcher
├── kraftbeat.spec          # PyInstaller config
├── build.bat               # Build script
└── README.md
```

---

## 6. Development Workflow

1. **Primary Testing**: DirectML on AMD GPU (Windows)
2. **CI/CD**: Test CUDA and CPU backends
3. **Release**: Multi-platform executables via PyInstaller
