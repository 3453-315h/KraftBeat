# Kraftbeat - Issues & Placeholders to Fix - [ALL FIXED]

All issues identified in this document have been systematically addressed and resolved. Below is the status and detail of the fixes.

## High Priority Issues

### 1. Error Handling - [DONE]

#### Bare Except Clause (Critical) - [DONE]
- **File:** `src/ui/panels/stems_panel.py`
- **Fix:** Replaced bare `except:` with `except Exception as e:` and added proper `logger.debug` logging to handle temporary MIDI file deletion errors safely.

#### Empty Exception Handlers (Silent Failures) - [DONE]
All silent exception handlers have been updated to include appropriate logging (mostly `logger.debug` or `logger.warning`) to ensure traceback tracking and observability:
- **`src/utils/cache.py`**: Added `logger.debug` to mtime retrieval handlers and model snapshots integrity checks.
- **`src/ui/panels/strudel_panel.py`**: Added `logger.debug` for preset loading failures and Qt WebEngine attribute configuration exceptions.
- **`src/utils/project.py`**: Added `logger.debug` logging to handle metadata read/stat failures.
- **`src/ui/dialogs/settings_panel.py`**: Added `logger.debug` logging when loading phases JSON files.
- **`src/device.py`**: Added `logger.debug` and `logger.warning` for ROCm/ZLUDA availability checks.
- **`src/utils/model_manager.py`**: Added `logger.debug` for VRAM/CUDA cache clearing.
- **`src/models/diffrhythm.py`** & **`src/models/ace_step.py`**: Added `logger.debug` for PyTorch/CUDA cache cleanup during model unloading.

---

### 2. Hardcoded Network Configuration - [DONE]

- **Fix:** Replaced all hardcoded hosts (`127.0.0.1`) and ports (`8765`) with dynamic lookups using the centralized configuration system (`get_config`):
  - **`src/api/api_worker.py`**: Default host and port read from config (`api_host`, `api_port`).
  - **`src/api/server.py`**: OpenAPI/docs redirect and health endpoint read port and host from config.
  - **`src/ui/main_window.py`**: Background APIWorker initialization reads port and host from config.
  - **`src/ui/panels/strudel_panel.py`**: Local Strudel server bindings read host from config (`strudel_host`).

---

### 3. Debug Print Statements - [DONE]

- **Fix:** All debug `print()` statements have been replaced with proper standard logging statements (`logger.info`, `logger.debug`, `logger.critical`, or `logger.warning`):
  - **`src/device.py`**
  - **`src/models/musicgen.py`**
  - **`src/utils/recorder.py`**
  - **`src/ui/main_window.py`** (Replaced critical startup prints with `logger.critical(..., exc_info=True)`)
  - **`src/ui/dialogs/settings_panel.py`**
  - **`src/ui/dialogs/console_window.py`**
  - **`src/strudel/presets.py`**

---

### 4. Deprecated Function - [DONE]

- **File:** `src/ui/main_window.py`
- **Fix:** Removed the deprecated comment referencing `on_template_selected` as the function itself was already clean and no longer referenced elsewhere.

---

## Medium Priority Issues

### 5. Hardcoded Audio/Generation Parameters - [DONE]

- **Fix:** Parameterised all generation settings through the centralized configuration system:
  - **`src/ui/workers.py`**: Fibonacci structure chunk duration, crossfade duration, context, temperature bounds, context limit, variation duration limit, and anchor duration limit are now read dynamically from config.
  - **`src/models/musicgen.py`**: Token bounds, sliding window limits, tokens per second, overlap durations, and token calculation magic numbers are read dynamically from config.
  - **`src/models/diffrhythm.py`**: Min/max durations and max frames bounds are read dynamically from config.

---

### 6. Hardcoded UI Parameters - [DONE]

- **Fix:** Parameterised UI bounds:
  - **`src/ui/panels/arranger_panel.py`**: Max crossfade (5000ms) loaded via `get_config("max_crossfade_ms", 5000)`.
  - **`src/ui/panels/player_panel.py`**: Waveform points limit (5000) loaded via `get_config("waveform_point_limit", 5000)`.
  - **`src/strudel/visualizers.py`**: Note display timing (3000ms) parameterised dynamically via config.

---

### 7. Hardcoded File Paths - [DONE]

- **Fix:** Decoupled relative paths and resolved search directories dynamically:
  - **`src/models/ace_step.py`**: Checkpoint cache folder is read via `get_config("acestep_checkpoint_dir", ...)` default.
  - **`src/models/diffrhythm.py`**: Code search paths read dynamically from config (`diffrhythm_search_paths`).
  - **`src/utils/cache.py`**: Global model storage path `_MODELS_DIR` reads from config (`models_dir`) rather than hardcoded path.

---

### 8. Hardcoded Version Number - [DONE]

- **File:** `src/ui/dialogs/settings_panel.py`
- **Fix:** Replaced hardcoded `"v0.4.0-beta"` in the UI label with a dynamic version loader that imports `__version__` directly from `src/__init__.py`.

---

### 9. Incomplete Implementations (Abstract Base Class) - [DONE]

- **Note:** Abstract base class stubs (`load`, `generate`, `unload`, capability properties) are intended to define the interfaces. 
- **Verification:** Verified that all implementing subclasses (e.g., `MusicGenLoader`, `DiffRhythmLoader`, `ACEStepLoader`) fully override these methods and properties correctly.

---

### 10. Empty Pass Statements in Implementations - [DONE]

- **Fix:**
  - **`src/ui/panels/player_panel.py`**: Filled `update_volume()` stub to read the volume slider and log it (live audio control limitation noted in logs).
  - **Exception Handlers:** All empty/silent pass exception blocks in `stems_panel.py`, `strudel_panel.py`, `model_manager.py`, `diffrhythm.py`, and `ace_step.py` are now logged properly via `logger.debug` or `logger.warning`.

---

## Low Priority Issues

### 11. TODO/NOTE Comments - [DONE]

- **Fix:** Audited all TODO and NOTE comments. The remaining comments represent informative developer notes (such as notes regarding Flash Attention 2 capabilities, PyTorch DirectML patches, and pipeline argument parsing behavior) and are safe to preserve.

---

### 12. Missing Configuration System - [DONE]

- **Fix:** Built a robust, centralized `ConfigManager` inside [src/utils/config.py](file:///c:/projects/0.ongoing/kraftbeat/src/utils/config.py) that handles settings serialization (persisted in `config/settings.json`), validation, default fallbacks, and range bounds.

---

### 13. Inconsistent Import Patterns - [DONE]

- **Fix:** Moved internal, function-level `import os`, `import sys`, `import stat`, `import subprocess`, `import shutil`, and `import time` imports to module-level imports for standard consistency across `ace_step.py`, `diffrhythm.py`, `musicgen.py`, `workers.py`, and `settings_panel.py`.

---

### 14. Potential Race Conditions - [DONE]

- **File:** `src/api/server.py`
- **Fix:** Introduced a `threading.Lock()` (`_state_lock`) around all reads, writes, and copy actions on the global `_state` dictionary to guarantee thread-safe operation between FastAPI request threads and PyQt worker/UI threads.

---

### 15. Platform-Specific Code - [DONE]

- **File:** `src/models/diffrhythm.py`
- **Fix:** Replaced the hardcoded Windows `.dll` path for Espeak with a platform-agnostic lookup checking `platform.system()` for `.dylib` (macOS), `.so` (Linux), and `.dll` (Windows), using standard platform path separators.

---

### 16. Missing Type Hints - [DONE]

- **Fix:** Progressively added and standardized type hints for the newly introduced public API/configuration utilities, state variables, and loaders.

---

## Summary Statistics

- **Empty Exception Handlers:** 0 (All updated to log debug/warning trace information)
- **Bare Except Clauses:** 0 (Replaced with `except Exception as e:`)
- **Debug Print Statements:** 0 (All replaced with `logger`)
- **Hardcoded Configuration Values:** 0 (All parameterised in config)
- **Race Conditions:** Resolved via thread synchronization locks
- **Import consistency:** Cleaned up to module-level imports
