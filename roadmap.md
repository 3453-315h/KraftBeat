# Kraftbeat Feature Roadmap

## 🚀 Core Features (Phase 1)

### Audio Generation

1. **Audio playback** - Play generated audio directly in the app
2. **Waveform visualization** - Display audio waveform using pyqtgraph
3. **Spectrogram view** - Frequency visualization for audio analysis
4. **Auto-save outputs** - Automatically save to `outputs/` folder with timestamps
5. **Generation queue** - Queue multiple prompts for batch generation

### Model Management

6. **Model download progress** - Show download progress bar for large models
7. **Model cache manager** - View/clear cached models to free disk space
8. **Lazy model loading** - Only load model when first generation requested

---

## 🎹 Music Features (Phase 2)

### Melody Conditioning

11. **Audio file input** - Drag-and-drop melody file for conditioning
12. **Microphone recording** - Record melody directly in app
13. **Humming detection** - Process hummed melodies for conditioning
14. **MIDI input** - Accept MIDI files as melody source
15. **Chroma extraction visualization** - Show extracted chroma features

### Generation Control

16. **Continuation mode** - Extend existing audio clips
17. **Seamless looping** - Generate audio that loops seamlessly
18. **BPM control** - Target specific tempo
19. **Key/scale selection** - Target specific musical keys
20. **Structure templates** - Intro/verse/chorus patterns

---

## 🎨 UI/UX Features (Phase 3)

### Interface Improvements

21. **Prompt history** - Save and recall previous prompts
22. **Prompt templates** - Genre-specific prompt starters
23. **Clean sidebar icons** - Minimal outline-style icons
24. **Resizable panels** - Drag to resize UI sections
25. **Keyboard shortcuts** - Space=play, Ctrl+G=generate, etc.

### Workflow Features

26. **Project files** - Save/load entire session state
27. **Generation history** - Timeline of all generated clips
28. **Favorites** - Star and organize best generations
29. **Tags and notes** - Annotate generated audio
30. **Export presets** - Save audio export settings (format, bitrate)

---

## ⚡ Performance Features (Phase 4)

### Optimization

31. **CUDA support** - Full NVIDIA GPU acceleration
32. **Multi-GPU** - Distribute across multiple GPUs
33. **Quantization (8-bit/4-bit)** - Reduce VRAM usage
34. **Flash Attention 2** - Faster attention when available
35. **Streaming generation** - Play audio as it generates

### Caching

36. **Prompt embedding cache** - Cache text embeddings
37. **KV-cache persistence** - Speed up continuation
38. **Audio chunk reuse** - Smart caching for similar prompts
39. **Precomputed audio starts** - Fast initial generation
40. **Memory profiling** - Monitor VRAM/RAM usage

---

## 🔧 Advanced Features (Phase 5)

### Audio Processing

41. **Post-processing effects** - Reverb, EQ, compression
42. **Stem separation** - Split generated audio into stems
43. **Audio mastering** - Loudness normalization, limiter
44. **Format conversion** - WAV, MP3, FLAC, OGG, OPUS
45. **Sample rate conversion** - Resample to target rate

### API & Integration

46. **REST API server** - HTTP API for external tools
47. **WebSocket streaming** - Real-time audio streaming
48. **CLI mode** - Command-line generation
49. **Plugin system** - Extensible architecture
50. **DAW integration** - VST/AU plugin wrapper

---

## 🔬 Experimental Features (Future)

### Next-Generation

- **Video sync** - Generate music synced to video
- **Real-time jamming** - Interactive continuous generation
- **Voice cloning** - Add vocal tracks with specific voices
- **Style transfer** - Apply style from reference audio
- **Multi-track composition** - Generate multiple stems simultaneously

### AI Enhancements

- **Prompt suggestions** - AI-powered prompt improvement
- **Auto-variation** - Generate multiple variations automatically
- **Quality scoring** - Rate generation quality
- **Feedback learning** - Learn from user preferences
- **Fine-tuning** - Train on user's audio samples

---

## 🚀 December 2025 - State of Long-Form AI Music

### Released Models (Available Now)

| Model | Duration | Status | Notes |
|-------|----------|--------|-------|
| **Suno V5** | Full songs | ✅ Released Sept 2025 | Pro/Premier subscribers, "Suno Studio" DAW announced |
| **Udio Sessions** | 2m10s clips, extendable | ✅ Released June 2025 | DAW-like editor, UMG licensed data (Nov 2025) |
| **Stable Audio 2.5** | 3 min @44.1kHz | ✅ Released Sept 2025 | Audio inpainting, <2s generation on GPU |
| **Stable Audio Open Small** | 11s | ✅ Released July 2025 | Mobile-optimized, open source |
| **MusicGen (Audiocraft)** | 5 min via chunking | ✅ Working | Chunks 8-21s, stitched. Coherence limited by 30s training. |

### Open Source Models (Local/Offline) - **PRIORITY FOR KRAFTBEAT**

| Model | Duration | VRAM | Features |
|-------|----------|------|----------|
| **ACE-Step** | Full songs | ~8GB | Suno-quality, multilingual, vocal cloning, style transfer |
| **DiffRhythm** | 4m45s in 10s | ~12GB | Latent diffusion, synchronized vocals/instrumentals |
| **Yue AI** | 5 min | ~10GB | Vocal + accompaniment from lyrics, Apache 2.0 license |
| **MusicGen** | 5 min | 4-8GB | Current Kraftbeat backend, reliable |

### Techniques Implementable NOW

1. **ACE-Step Integration** (Priority #1)
   - Open source Suno alternative
   - Produces full songs with vocals
   - Could replace MusicGen for long-form

2. **DiffRhythm Integration** (Priority #2)
   - 4m45s coherent generation in 10 seconds
   - Diffusion-transformer architecture
   - Synchronized vocals and instrumentals

3. **Two-Pass Refinement** (Quick Win)
   - Generate rough → Use as audio prompt → Generate polished
   - Works with current MusicGen

4. **Stable Audio Open Small** (Mobile)
   - 11s on-device generation
   - Good for previews/sketches

5. **Enhanced Audio Inpainting** (From Stable Audio 2.5)
   - Fill gaps in generated audio
   - Extend sections intelligently

### Suno V5 Features (Competitor Analysis)

- **Intelligent Composition Architecture**: Better musical structure
- **Adaptive Creative Intelligence**: Remembers voice/instrument preferences
- **Persistent Memory**: Consistent style across generations
- **Suno Studio (DAW)**: Restructure songs, add/remove components
- **Professional Control Suite**: Fine-tune musical aspects

### Udio Sessions Features (Competitor Analysis)

- **DAW-like Editor**: Edit, extend, replace sections
- **Takes System**: Multiple versions of each section
- **Advanced Parameters**: BPM, key, instrumentation, complexity
- **Licensed Training Data**: UMG partnership (Nov 2025)

### Future Kraftbeat Goals (Updated)

- [x] **ACE-Step Backend** - Add as alternative model for full songs
- [x] **DiffRhythm Backend** - 4m45s coherent generation
- [ ] **10+ minute chaining** - Intelligent chunk stitching
- [ ] **Vocal synthesis** - Integrate with vocal models
- [ ] **Audio inpainting** - Fill gaps, extend sections
- [ ] **DAW-like editor** - Similar to Suno Studio/Udio Sessions
- [ ] **Model fine-tuning** - Train on user's music

---

## Priority Legend

| Priority | Meaning |
|----------|---------|
| 🔴 High | Essential for usability |
| 🟡 Medium | Nice to have |
| 🟢 Low | Future consideration |

## Current Status

### Completed ✅ (35+)

**Core**: DirectML GPU, MusicGen, PyQt6, console
**Audio**: Playback, waveform, spectrogram, auto-save, history, melody drop, volume, loop
**UI**: Sidebar, templates, shortcuts, themes, polish (gradients)
**Music**: BPM (20-300), key/scale, continuation, seamless loop, favorites, notes, queue

**New Features**:

- 🎚️ Stems Panel - Multi-track stem generation (5 tracks)
- 🚀 CUDA Backend - Full NVIDIA GPU support (requirements/cuda.txt)
- ⚡ Flash Attention 2 - Optimized transformer attention for faster generation
- 📉 Quantization - 4-bit, 8-bit, and FP16 precision modes for lower VRAM
- 🎛️ Effects - Reverb, Compression, Bass/Treble EQ
- 💽 Format Export - WAV, MP3, FLAC, OGG with bitrate
- 📋 Project Files - Save/load session state (.kraftbeat)
- ♾️ **Infinite Mode** - Generate tracks of **any length** (e.g. 5 mins) by chaining 30s segments
- 🎼 **Smart Structure** - Automatically structures long songs (Intro → Verse → Chorus → Outro) when "Full Song" is selected
- 📦 Model Download Progress - Visual tracking in Model Manager
- 💡 Solutions Tab - Dedicated help/fix tab in Settings
- 🎵 Audio Import - Import audio files as generation seeds
- 🎲 Auto-Variation - Generate and compare multiple variations (auto-saved to outputs/variations/)
- 🎼 Structure Presets - 20+ templates (Intro, Verse, Chorus, Drop, Build-up, Full Song, EDM Track, etc.)
- 🖥️ GPU Settings Tabs - Dedicated DirectML, CUDA, ROCm tabs with specific options
- 🟣 ROCm Windows Support - Preview support for RX 7000/9000 & Ryzen AI (requirements/rocm.txt)
- 🖤 Dark Theme Only - Clean, modern dark interface
- 📦 Model Manager - Improved with proper model names, quality/speed ratings, family grouping
- 📁 Local Models - Models stored in project `./models/` folder (portable)
- 🎤 **ACE-Step Integration** - Full song generation with vocals
- 🥁 **DiffRhythm Integration** - Long-form diffusion generation (4m45s)
- 🎹 **Strudel Live Coding** - Embedded algorithmic music with:
  - 📦 Offline-ready bundled Strudel
  - 🎼 **135+ Pattern Presets** across 10 genres (Techno, House, DnB, Hip-Hop, Ambient, World, Experimental, Classic, Dubstep, Lo-Fi)
  - 🎨 **8 Visual Themes** (Kraftbeat, Neon Nights, Forest, Ocean, Fire, Midnight, Sunrise, Arctic)
  - 📀 **22 Sample Packs** downloadable on-demand (Drum Machines, Dirt, VCSL Orchestra, World, etc.)
- ⬇️ **One-Click Model Install** - Auto-download weights and dependencies from UI

**Dynamic Structure Engine (v2.0)**:

- 🎼 **Phase Count System** - 8/10/13/21 phase configurations (Fibonacci)
- 📐 **Golden Ratio Positioning** - Bridge/climax at φ (61.8%)
- 🧠 **Smart Self-Aware Prompts** - Auto-appends phase/energy/position/temp/bpm/key metadata
- 📝 **Sub-Prompts** - Each phase has evolving sub-prompts for multi-chunk phases
- 🎛️ **BPM/Key UI Controls** - Spinbox (0-300) and dropdown (24 keys)
- 🌡️ **Energy-Based Temperature** - Gaussian curve centered at golden ratio
- 🎼 **Phases Editor** - Settings → 🎼 Phases tab with genre presets (EDM/Jazz/Ambient)
- 📂 **Phase Config Files** - `config/phases_8.json`, `phases_10.json`, `phases_13.json`, `phases_21.json`

**Refactoring**: workers.py, themes.py, panels/, effects.py, project.py, device.py

### Remaining 🔄

- Package for distribution
