# Kraftbeat - AI Music & Vocal Generator

A comprehensive AI music creation suite powered by **MusicGen**, **ACE-Step**, and **DiffRhythm**.  
Generate instrumentals, full songs with vocals, and long-form compositions up to **10 minutes**.

GPU-accelerated with DirectML/CUDA/ROCm/ZLUDA support for AMD, NVIDIA, and Intel GPUs.

## Features (45+)

### Generation

- 🎵 Text-to-music with melody conditioning
- ⏱️ **Extended Duration** - Generate up to 10 minutes (600s)
- 🌊 **Streaming** - Real-time audio playback during generation
- 🥁 BPM control (20-300), Key/scale selector (24 keys)
- ➡️ **Infinite Continuation** - Generate tracks > 30s with **Dynamic Structure Engine**:
  - 🎼 **10-Phase System**: Intro → Verse → Pre-Chorus → Chorus → Bridge → Climax → Outro
  - 📐 **Golden Ratio Positioning**: Bridge/climax at φ (61.8%) of song
  - 🔢 **Fibonacci Chunk Modes**: Coherent (8s), Balanced (13s), Speed (21s)
  - 🧠 **Smart Self-Aware Prompts**: Auto-appends phase/energy/position metadata
- 🔁 Seamless loop option
- 🎠 **Block Arranger** - Stack, reorder, and crossfade generated audio blocks into a final track
  - 🤚 **Drag & Drop** to reorder blocks with pixel-perfect preview
  - ✨ **Crossfade Engine**: Configurable overlap (0–5000ms) with overlap-add blending
  - 🌟 **Quick Fill**: Load all recent generations from `outputs/` in one click
  - 💾 **One-Click Render**: Normalize, stitch, and export to WAV with the global player pre-loaded
- 🎚️ **Stems Panel** - Multi-track stem separation (Vocals/Drums/Bass/Other)
  - 🎹 **Audio-to-MIDI**: Extract polyphonic MIDI directly from isolated stems (Powered by Spotify's basic-pitch)
- 🎲 **Variations** - Generate multiple variations to compare (auto-saved)
- 🎤 **ACE-Step Integration** - Generate full songs with **Vocals** and lyrics
  - 🎙️ **The Voice Lab**: Dedicated UI to extract, save, and manage custom voice clones from any acapella audio file
  - 🌟 **New v1.5 Models**: Support for ACE-Step 1.5 XL Turbo and SFT for ultra-realistic vocal dynamics
  - 🎨 **100+ Style Presets**: Pop, Rock, Jazz, Electronic, Hip-Hop, Classical, World, and more
  - 🎵 **Audio2Audio**: Use reference audio to guide generation style
  - 💾 **Auto-Save**: Generated audio automatically saved to `outputs/` with timestamps
- 🥁 **DiffRhythm Integration** - Long-form generation (4m 45s) using latent diffusion
  - 🎼 **DiffRhythm Full**: Support for the uncompressed, high-fidelity full-length model
  - 🎨 **60+ Style Presets**: Organized by genre, era, and vocal style
  - ⚙️ **Parameters**: Steps (8-64), CFG strength (1.0-8.0), Seed
- 🎹 **Strudel Live Coding** - Embedded algorithmic music environment
  - 📦 **Offline Mode**: Bundled for exe compilation, works without internet
  - 🎼 **135+ Pattern Presets**: Techno, House, DnB, Hip-Hop, Ambient, World, Experimental, Classic, Dubstep, Lo-Fi (Production-Quality)
  - 🎨 **8 Visual Themes**: Kraftbeat, Neon Nights, Forest, Ocean, Fire, Midnight, Sunrise, Arctic
  - 📀 **22 Downloadable Sample Packs**: Drum machines, Dirt-Samples, Piano, VCSL Orchestra, and more
  - 📊 **Visualizers**: Oscilloscope and spectrum analyzer (toggle with 📊 button)
  - 📝 **Code Snippets**: 10+ ready-to-use patterns for drums, bass, chords, melody
  - 🎹 **MIDI Input**: Connect MIDI keyboard via Web MIDI API (toggle with 🎹 button)
  - 🔊 **TidalCycles Patterns**: Create beats with `s("bd sd hh")`
- 🎼 **Phases Editor** - Customize phase modifiers in Settings → 🎼 Phases (EDM/Jazz/Ambient presets)

### Performance & Compute

- ⚙️ **Settings Dialog** - General, Audio, Solutions, and **GPU-specific tabs**
- 🧠 **Deep VRAM Optimizations**: Aggressive Garbage Collection and Dynamic KV Caching explicitly configured to allow massive 3.3B+ parameter models to run flawlessly on 8GB VRAM setups
- 💡 **Solutions Tab** - Quick fixes for common issues (e.g., Memory/Quantization, CPU Offloading)
- 🖥️ **Compute Backend** - Explicit selection with dedicated settings:
  - **DirectML**: Default for AMD/Intel on Windows (Fixed native GPU execution, no CPU fallbacks!)
  - **CUDA**: Native NVIDIA support (FP16, Flash Attention, torch.compile)
  - **ROCm**: AMD Native - **Now with Windows 11 Preview support!** (RX 7000/9000, Ryzen AI)
  - **ZLUDA**: Drop-in CUDA support for AMD (requires external setup)
- ⚡ **8-bit Quantization** - Reduces VRAM usage by ~50%
- 📦 **Model Manager** - Download and manage AI models + Strudel sample packs
- ⬇️ **Easy Install** - Download via UI (Model Manager) or CLI (`download_models.bat`)

### Model Types

| Model | Purpose | Speed | VRAM | Stereo | Melody |
|-------|---------|-------|------|--------|--------|
| **MusicGen** | High-quality music | Slow | 4-18GB | ✅ (variants) | ✅ (melody variant) |
| **AudioGen** | Sound effects (foley, ambiance) | Slow | 8GB | ❌ | ❌ |
| **MAGNeT** | Fast music generation | **7x faster** | 4-8GB | ❌ | ❌ |
| **ACE-Step** | Songs with **Vocals** (up to 4 min) | Medium | ~6GB | ✅ | Audio2Audio |
| **DiffRhythm** | Long-Form (4m45s fixed) | **Fast** (~10s) | ~8GB | ✅ | ❌ |

**Recommendation**: Use `musicgen-stereo-medium` for quality, `magnet-medium-30s` for speed, `audiogen` for SFX.

### Post-Processing

- 🎛️ **Effects** - Reverb, Compression, Bass/Treble EQ
- 💽 **Multi-Format Export** - WAV, MP3, FLAC, OGG (128k-320k)

### UI/UX

- 🖤 **Dark Theme** - Modern dark interface designed for long sessions
- 🎤 **Mic Recording** - Record melody ideas directly in app
- 📊 **Memory Monitor** - Real-time RAM/VRAM usage tracking in status bar
- 📦 **Model Manager** - Download and manage AI models (stored in project `./models/` folder)
- 📋 Project Files (.kraftbeat), Notes, Tags, Shortcuts
- 🌐 **Headless REST API** - Embedded FastAPI server for external control and DAW scripting

## Quick Start

```bash
# GUI (Windows Virtual Environment)
.\run.bat

# CLI
python -m src.cli "ambient chill" -d 60 -o chill.wav
```

> **Note:** Kraftbeat v0.4.0 completely patches DirectML instability without resorting to CPU fallbacks! You now get 100% native GPU acceleration on AMD and Intel cards.

## REST API (DAW Integration)

Kraftbeat automatically starts a **local REST API** on port `8765` when launched. This allows headless generation from any DAW script, Python automation, or OBS plugin.

Interactive API docs are always available at: **http://localhost:8765/docs**

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Health check |
| `GET`  | `/models` | List all available models |
| `POST` | `/generate` | Start a generation job |
| `GET`  | `/status` | Poll job status / get output path |
| `POST` | `/stop` | Cancel the current generation |
| `GET`  | `/outputs` | List all files in `./outputs/` |

### Example: Generate from a Python Script

```python
import requests, time

# Start generation
res = requests.post("http://localhost:8765/generate", json={
    "prompt": "lo-fi hip hop, chill, vinyl crackle",
    "duration": 30
})
job_id = res.json()["job_id"]

# Poll until done
while True:
    status = requests.get(f"http://localhost:8765/status").json()
    if status["status"] in ("complete", "error"):
        print("Output:", status["output_path"])
        break
    time.sleep(2)
```


## GPU Setup

### DirectML (AMD/Intel - Default)

Already included. Works out of the box on Windows.

### CUDA (NVIDIA)

For native NVIDIA support with Flash Attention 2 and FP16/INT8 optimization:

```bash
pip install -r requirements/cuda.txt
```

### ROCm (AMD Native - Windows 11 Preview)

1. Install AMD PyTorch Preview Driver from [AMD.com](https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html)
2. `pip install -r requirements/rocm.txt`
3. **Requirements**: Windows 11, RX 7000/9000 series or Ryzen AI APU

### ROCm (AMD - Linux)

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2
```

### ZLUDA (AMD via CUDA translation)

1. Download ZLUDA binaries
2. Run: `zluda.exe -- python -m src.ui.main_window`
3. Select "ZLUDA" in Settings > Compute

## License

MIT

## Architecture & Internals

### High-Level Architecture

Kraftbeat is built on a modular architecture using **PyQt6** for the frontend and **PyTorch/DirectML** for the backend.

- **Frontend (UI)**:
  - `src/ui/main_window.py`: Central hub managing views (`QStackedWidget`), themes, and global state.
  - `src/ui/workers.py`: dedicated `QThread` workers for non-blocking generation, model loading, and variation processing.
  - `src/ui/panels/`: Modular components (Stems Mixer, Cache Manager).
- **Backend (Core)**:
  - `src/models/musicgen.py`: Unified API wrapper handling both `audiocraft` (Meta) and `transformers` (Hugging Face) libraries.
  - `src/device.py`: Intelligent hardware acceleration detection (DirectML vs CUDA vs CPU).
  - `src/utils/`: Specialized utilities for audio processing (`audio.py`), streaming (`streaming.py`), and project management.

### The Generation Pipeline

1. **Input Processing**:
    - User inputs prompt, parameters (BPM, Key), and optional audio melody.
    - `MainWindow` validates inputs and instantiates a `GenerationWorker`.

2. **Model Loading Strategy** (`MusicGenLoader`):
    - **Smart Backend Selection**: Automatically detects GPU type:
      - **NVIDIA**: Defaults to `audiocraft` (CUDA optimized).
      - **AMD/Intel (DirectML)**: Defaults to `transformers` (DirectML optimized) to ensure GPU acceleration and avoid CPU fallbacks.
      - **MAGNeT Models**: Experimental Support via patched `audiocraft` on DirectML.
    - **Resilient Download**: Implements a "Flat Directory" fallback if Windows symlink creation fails (WinError 1314), ensuring models are always usable.

3. **Dynamic Structure Engine** (Infinite Mode):
    - **Fibonacci Chunk Modes** (Settings → Audio):
      - 🎯 **Coherent (8s)**: Maximum control, tightest structure, 21 phases
      - ⚖️ **Balanced (13s)**: Recommended - good coherence, 13 phases
      - ⚡ **Speed (21s)**: Fast generation, 8 phases
    - **Phase Count System** (Settings → 🎼 Phases):
      - Configurable phase counts: 8, 10, 13, or 21 phases
      - Each loads from `config/phases_X.json`
      - Phases include **sub-prompts** for evolution within each phase
    - **Golden Ratio Positioning**: Bridge/climax at φ (61.8%)
    - **Smart Self-Aware Prompts**: Each chunk's prompt includes:

      ```text
      [user prompt], [phase modifier], [sub-prompt] | [STRUCTURE: phase=X, chunk=N/M, position=XX%, energy=0.XX, temp=X.XX, bpm=120, key=Am]
      ```

    - **BPM/Key Controls**: UI spinbox (0-300) and dropdown (24 keys + Auto)
      - Priority: UI controls → Prompt extraction → Model decides
    - **Energy-Based Temperature**: Gaussian curve centered at φ
    - **Anchor Injection**: First 10s saved, re-injected at Bridge
    - **Live Phase Indicator**: 🎬 INTRO, 📖 VERSE, 🎵 CHORUS, 🌉 BRIDGE, 🔥 CLIMAX, 🌅 OUTRO

4. **Audio Output**:
    - Audio normalized and converted to numpy arrays
    - Crossfading between chunks eliminates clicks/pops
    - **Real-time Streaming**: `StreamingGenerator` pushes PCM to `sounddevice`
    - Final artifacts saved to `./outputs/` with JSON metadata

## Configuration Files

| File | Purpose |
|------|---------|
| `config/phases.json` | Default 10-phase configuration |
| `config/phases_8.json` | 8 phases for Speed mode |
| `config/phases_10.json` | 10 phases (Default) |
| `config/phases_13.json` | 13 phases for Balanced mode |
| `config/phases_21.json` | 21 phases for Coherent mode |
