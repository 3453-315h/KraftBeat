"""
Kraftbeat - Background Workers

Worker threads for model loading and audio generation.
"""

import logging
import os
import stat
import subprocess
import shutil
import time
from PyQt6.QtCore import QThread, pyqtSignal, QMetaObject, Qt, Q_ARG

from pathlib import Path
from src.models.musicgen import MusicGenLoader
from utils.config import get_config

logger = logging.getLogger(__name__)


class QTextEditLogger(logging.Handler):
    """Custom logging handler that writes to a QTextEdit widget (thread-safe)."""
    
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%H:%M:%S'
        ))
    
    def emit(self, record):
        msg = self.format(record)
        # Thread-safe update using QMetaObject
        if self.widget:
            QMetaObject.invokeMethod(
                self.widget, "append",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, msg)
            )


class GenerationWorker(QThread):
    """Background worker for audio generation."""
    
    finished = pyqtSignal(object)  # numpy array or None
    progress = pyqtSignal(int)
    error = pyqtSignal(str)
    status = pyqtSignal(str)
    
    def __init__(self, loader: MusicGenLoader, params: dict):
        super().__init__()
        self.loader = loader
        self.params = params
        
    def run(self):
        try:
            self.status.emit("Generating audio...")
            
            # Check for infinite mode and structured mode
            # Note: We pop them because loader.generate doesn't expect these args
            infinite_mode = self.params.pop('infinite_mode', False)
            structured_mode = self.params.pop('structured_mode', False)
            structure_mode = self.params.pop('structure_mode', 'balanced')  # Fibonacci preset
            total_duration = self.params.get('duration', 10.0)
            
            # Standard single pass if:
            # 1. Short duration (<= 30s), OR
            # 2. Not infinite mode, OR
            # 3. Long duration but NOT structured mode (use native audiocraft long-form)
            if not infinite_mode or total_duration <= 30.0:
                audio = self.loader.generate(**self.params)
                if audio is not None:
                    self.finished.emit(audio)
                else:
                    self.error.emit("Generation returned no audio")
                return
            
            # Long-form generation: Choose between native or structured
            if not structured_mode:
                # NATIVE LONG-FORM: Just use audiocraft's built-in long-form capability
                # audiocraft handles sliding window internally when duration > 30s
                logger.info(f"Using NATIVE audiocraft long-form generation ({total_duration}s)")
                self.status.emit(f"Generating {total_duration}s (native mode)...")
                audio = self.loader.generate(**self.params)
                if audio is not None:
                    self.finished.emit(audio)
                else:
                    self.error.emit("Generation returned no audio")
                return

            # Infinite Generation Logic
            import numpy as np
            full_audio = None
            
            # ==================================================================================
            # FIBONACCI-BASED CHUNK DURATIONS (Golden Ratio Structure)
            # Using Fibonacci numbers: 8, 13, 21 for musically meaningful proportions.
            # ==================================================================================
            
            # Fibonacci Presets (structure_mode was already popped at the top)
            if structure_mode == 'coherent':
                CHUNK_DURATION = get_config("chunk_duration_coherent", 8.0)
                CROSSFADE_SECONDS = get_config("crossfade_coherent", 1.0)
                CONTEXT_SECONDS = get_config("context_coherent", 5.0)
            elif structure_mode == 'speed':
                CHUNK_DURATION = get_config("chunk_duration_speed", 21.0)
                CROSSFADE_SECONDS = get_config("crossfade_speed", 3.0)
                CONTEXT_SECONDS = get_config("context_speed", 13.0)  # Fibonacci!
            else:  # 'balanced' (default)
                CHUNK_DURATION = get_config("chunk_duration_balanced", 13.0)
                CROSSFADE_SECONDS = get_config("crossfade_balanced", 2.0)
                CONTEXT_SECONDS = get_config("context_balanced", 8.0)   # Fibonacci!
            
            logger.info(f"Structure Mode: {structure_mode} (Chunk: {CHUNK_DURATION}s, Crossfade: {CROSSFADE_SECONDS}s)")
            
            # Calculate effective new audio per chunk (after first)
            EFFECTIVE_NEW_AUDIO = CHUNK_DURATION - CROSSFADE_SECONDS
            
            # Calculate how many chunks we need
            if total_duration <= CHUNK_DURATION:
                num_chunks = 1
            else:
                remaining_after_first = total_duration - CHUNK_DURATION
                additional_chunks = int(np.ceil(remaining_after_first / EFFECTIVE_NEW_AUDIO))
                num_chunks = 1 + additional_chunks
            
            current_chunk_idx = 0
            base_temperature = self.params.get('temperature', 1.0)
            
            # ==================================================================================
            # DYNAMIC STRUCTURE ENGINE
            # Logic to create non-linear, structured songs based on total duration.
            # Phases are now driven by the prompt list from main_window.py
            # which uses golden-ratio positioning for phase transitions.
            # ==================================================================================

            anchor_audio = None
            
            # Check if we have a dynamic prompt list (from golden-ratio system)
            base_prompt = self.params.get('prompt', '')
            prompt_list = None
            if isinstance(base_prompt, list):
                prompt_list = base_prompt
                logger.info(f"Using dynamic prompt list with {len(prompt_list)} prompts")
            else:
                logger.info(f"Using static prompt: {base_prompt[:50]}...")
            
            logger.info(f"Generating song structure: {total_duration}s ({num_chunks} chunks)")

            for i in range(num_chunks):
                if self.isInterruptionRequested():
                    logger.info("Generation interrupted by user.")
                    break
                
                # Dynamic Phase Calculation (Extended Fluid Structure)
                # Determines the musical function of the current chunk
                
                phase_name = "BODY"
                
                # Default Assignments
                is_intro = (i == 0)
                is_final = (i == num_chunks - 1)
                
                # Structured Logic based on Chunk Index
                if is_intro:
                    phase_name = "INTRO"
                elif is_final:
                    phase_name = "OUTRO"
                else:
                    # Middle Section Logic
                    # We want an oscillation: Verse -> Chorus -> Link -> Verse...
                    
                    # If we only have 3 chunks: Intro -> Body -> Outro
                    if num_chunks <= 3:
                        phase_name = "BODY/TRANSITION"
                    
                    # If we have 4+ chunks, we can build a structure
                    else:
                        # Golden Ratio Bridge Point (φ ≈ 0.618)
                        # This is where the natural "climax" or key change occurs in many compositions
                        bridge_idx = int(num_chunks * 0.618)
                        
                        if i == bridge_idx:
                            phase_name = "BRIDGE"
                        elif i < bridge_idx:
                            # Pre-Bridge: Verse/Chorus alternation
                            # i=1 (Verse), i=2 (Chorus), i=3 (Verse)...
                            if i % 2 != 0:
                                phase_name = "VERSE"
                            else:
                                phase_name = "CHORUS"
                        else:
                            # Post-Bridge
                            phase_name = "CHORUS/CLIMAX"

                # Enhanced Status with Phase Indicator
                phase_emoji = {"INTRO": "🎬", "VERSE": "📖", "CHORUS": "🎵", "BRIDGE": "🌉", 
                               "CHORUS/CLIMAX": "🔥", "OUTRO": "🌅", "BODY/TRANSITION": "➡️"}.get(phase_name, "🎶")
                self.status.emit(f"{phase_emoji} {phase_name} [{i+1}/{num_chunks}] - Generating...")
                
                # ----------------
                # ENERGY-BASED TEMPERATURE (Golden Ratio Curve)
                # ----------------
                import math
                
                # Calculate position and energy
                position = i / max(1, num_chunks - 1)
                PHI = 0.618
                
                # Gaussian energy curve centered at golden ratio
                energy = math.exp(-((position - PHI) ** 2) / 0.1)
                
                # Map energy (0-1) to temperature offset (-0.2 to +0.2)
                # High energy = higher temp (more creative), Low energy = lower temp (stable)
                temp_offset = (energy - 0.5) * 0.4  # Range: -0.2 to +0.2
                
                # Special cases for intro/outro
                if is_intro:
                    temp_offset = -0.1  # Stable start
                elif is_final:
                    temp_offset = -0.25  # Very stable ending
                    
                temp_min = get_config("temp_bound_min", 0.6)
                temp_max = get_config("temp_bound_max", 1.4)
                current_temp = max(temp_min, min(temp_max, base_temperature + temp_offset))
                
                logger.debug(f"Chunk {i+1}: pos={position:.2f}, energy={energy:.2f}, temp={current_temp:.2f}")
                
                audio_ctx = None
                
                # Context Window (Standard)
                if full_audio is not None and not is_intro:
                     # Default to last 15s connection
                     ctx_len_sec = get_config("context_length_limit", 15.0)
                     ctx_len = int(ctx_len_sec * self.loader.sample_rate)
                     audio_ctx = full_audio[:, -ctx_len:]

                # Phase-specific overrides
                if phase_name == "INTRO":
                    # Clean start
                    audio_ctx = None
                    
                elif phase_name == "BRIDGE":
                     # RECALL: Inject Anchor explicitly to ground the song before finale
                     if anchor_audio is not None:
                         logger.info("Injecting ANCHOR theme for Bridge/Breakdown...")
                         audio_ctx = anchor_audio 
                         current_temp += 0.1  # Extra chaos for bridge tension

                elif phase_name == "OUTRO":
                     # Longer context for smooth fade
                     if full_audio is not None:
                         outro_ctx_sec = get_config("variation_duration_limit", 20.0)
                         audio_ctx = full_audio[:, -int(outro_ctx_sec * self.loader.sample_rate):]

                self.params['duration'] = CHUNK_DURATION
                self.params['temperature'] = current_temp
                self.params['audio_prompt'] = audio_ctx
                
                # Use per-chunk prompt if we have a dynamic prompt list
                if prompt_list and i < len(prompt_list):
                    self.params['prompt'] = prompt_list[i]
                    logger.info(f"Chunk {i+1} prompt: {prompt_list[i][:60]}...")
                elif isinstance(base_prompt, str):
                    self.params['prompt'] = base_prompt
                
                chunk = self.loader.generate(**self.params)
                
                if chunk is None:
                    self.error.emit(f"Failed at chunk {i+1}")
                    return

                # Save Anchor (Intro)
                if is_intro:
                    # Save first 10s as anchor
                    # Ensure it's not too long for prompting
                    anchor_len_sec = get_config("anchor_duration_limit", 10.0)
                    anchor_len = int(anchor_len_sec * self.loader.sample_rate)
                    if chunk.shape[1] > anchor_len:
                         anchor_audio = chunk[:, :anchor_len]
                    else:
                         anchor_audio = chunk

                # Stitch with crossfade
                if full_audio is None:
                    full_audio = chunk
                else:
                    crossfade_samples = int(CROSSFADE_SECONDS * self.loader.sample_rate)
                    
                    if crossfade_samples > 0 and full_audio.shape[1] >= crossfade_samples and chunk.shape[1] >= crossfade_samples:
                        fade_out = np.linspace(1.0, 0.0, crossfade_samples)
                        fade_in = np.linspace(0.0, 1.0, crossfade_samples)
                        
                        if full_audio.ndim == 2:
                            fade_out = fade_out[np.newaxis, :]
                            fade_in = fade_in[np.newaxis, :]

                        # Blend region
                        end_prev = full_audio[:, -crossfade_samples:] * fade_out
                        start_next = chunk[:, :crossfade_samples] * fade_in
                        blended = end_prev + start_next
                        
                        full_audio = np.concatenate([
                            full_audio[:, :-crossfade_samples],
                            blended,
                            chunk[:, crossfade_samples:]
                        ], axis=1)
                    else:
                        full_audio = np.concatenate([full_audio, chunk], axis=1)
                
                # Progress update
                progress_pct = int(((i + 1) / num_chunks) * 100)
                self.progress.emit(progress_pct)
                
                current_chunk_idx += 1
            
            self.finished.emit(full_audio)
            
        except Exception as e:
            self.error.emit(str(e))


class ModelLoadWorker(QThread):
    """Background worker for model loading."""
    
    finished = pyqtSignal(bool)
    status = pyqtSignal(str)
    
    def __init__(self, loader: MusicGenLoader, model_name: str, precision: str = "fp32"):
        super().__init__()
        self.loader = loader
        self.model_name = model_name
        self.precision = precision
        
    def run(self):
        self.status.emit(f"Loading {self.model_name} model ({self.precision})...")
        success = self.loader.load_model(self.model_name, precision=self.precision)
        self.finished.emit(success)


class ModelDownloadWorker(QThread):
    """Background worker for model downloading."""
    
    finished = pyqtSignal(bool)
    status = pyqtSignal(str)
    
    def __init__(self, loader: MusicGenLoader, model_name: str):
        super().__init__()
        self.loader = loader
        self.model_name = model_name
        
    def run(self):
        self.status.emit(f"Downloading {self.model_name}...")
        success = self.loader.download_model(self.model_name)
        if success:
            self.status.emit("Download complete!")
        else:
            self.status.emit("Download failed.")
        self.finished.emit(success)


class VariationWorker(QThread):
    """Background worker for generating multiple variations."""
    
    variation_complete = pyqtSignal(int, object)  # (index, audio numpy array)
    all_complete = pyqtSignal(list)  # list of audio arrays
    progress = pyqtSignal(int)  # 0-100
    error = pyqtSignal(str)
    status = pyqtSignal(str)
    
    def __init__(self, loader: MusicGenLoader, params: dict, variation_count: int = 4):
        super().__init__()
        self.loader = loader
        self.base_params = params.copy()
        self.variation_count = variation_count
        
    def run(self):
        import random
        
        try:
            variations = []
            base_temp = self.base_params.get('temperature', 1.0)
            
            for i in range(self.variation_count):
                self.status.emit(f"Generating variation {i+1}/{self.variation_count}...")
                
                # Create variation params with different seed and temperature
                params = self.base_params.copy()
                
                # Vary temperature slightly (+/- 0.15 range)
                temp_offset = (i - self.variation_count / 2) * 0.08
                params['temperature'] = max(0.5, min(1.5, base_temp + temp_offset))
                
                # Add randomness via top_k variation
                params['top_k'] = random.randint(180, 250)
                
                # Remove infinite mode if present (we want short variations)
                params.pop('infinite_mode', None)
                
                # Generate
                audio = self.loader.generate(**params)
                
                if audio is not None:
                    variations.append(audio)
                    self.variation_complete.emit(i, audio)
                else:
                    self.error.emit(f"Variation {i+1} failed to generate")
                    return
                
                # Progress
                progress_pct = int(((i + 1) / self.variation_count) * 100)
                self.progress.emit(progress_pct)
            
            self.all_complete.emit(variations)
            self.status.emit(f"Generated {len(variations)} variations!")
            
        except Exception as e:
            self.error.emit(str(e))


class StrudelSampleDownloadWorker(QThread):
    """Background worker for downloading Strudel sample packs."""
    
    finished = pyqtSignal(bool)  # success/failure
    status = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, pack_key: str, pack_info: dict, target_dir):
        super().__init__()
        self.pack_key = pack_key
        self.pack_info = pack_info
        self.target_dir = Path(target_dir) / pack_key
    
    def _log_status(self, message: str):
        """Log status to both console and signal."""
        logger.info(f"[Strudel Samples] {message}")
        self.status.emit(message)
    
    def _remove_readonly(self, func, path, excinfo):
        """Error handler for shutil.rmtree to handle read-only files on Windows."""
        os.chmod(path, stat.S_IWRITE)
        func(path)
    
    def run(self):
        """Download sample pack from GitHub."""
        
        try:
            repo = self.pack_info.get('repo', '')
            branch = self.pack_info.get('branch', 'main')
            display_name = self.pack_info.get('display_name', self.pack_key)
            
            self._log_status(f"📦 Starting download: {display_name}")
            self._log_status(f"   Repository: github.com/{repo}")
            
            self.target_dir.mkdir(parents=True, exist_ok=True)
            
            # Clone via git (shallow clone for speed)
            repo_url = f"https://github.com/{repo}.git"
            temp_dir = self.target_dir.parent / f"_temp_{self.pack_key}"
            
            # Remove temp dir if it exists (with Windows-safe cleanup)
            if temp_dir.exists():
                self._log_status(f"   Cleaning up previous temp files...")
                try:
                    shutil.rmtree(temp_dir, onerror=self._remove_readonly)
                except Exception as e:
                    self._log_status(f"   Warning: Could not clean temp dir: {e}")
                    # Try again after a short wait
                    time.sleep(1)
                    try:
                        shutil.rmtree(temp_dir, onerror=self._remove_readonly)
                    except Exception as e:
                        logger.debug(f"Retry cleanup failed: {e}")
            
            self._log_status(f"⬇️ Downloading from GitHub (this may take a while)...")
            self.progress.emit(10)
            
            # Shallow clone with progress
            result = subprocess.run(
                ["git", "clone", "--depth", "1", "--branch", branch, "--progress", repo_url, str(temp_dir)],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode != 0:
                self._log_status(f"❌ Git clone failed: {result.stderr}")
                self.finished.emit(False)
                return
            
            self._log_status(f"✅ Clone complete, organizing samples...")
            self.progress.emit(50)
            
            # Move samples to target (handle subpath if specified)
            subpath = self.pack_info.get('subpath', '')
            source_dir = temp_dir / subpath if subpath else temp_dir
            
            # Copy all audio files
            audio_extensions = {'.wav', '.mp3', '.ogg', '.flac', '.aif', '.aiff'}
            copied_count = 0
            
            # Count total files first
            all_audio_files = [f for f in source_dir.rglob('*') 
                              if f.is_file() and f.suffix.lower() in audio_extensions]
            total_files = len(all_audio_files)
            
            self._log_status(f"   Found {total_files} audio files to copy...")
            
            for i, src_file in enumerate(all_audio_files):
                # Preserve relative structure
                rel_path = src_file.relative_to(source_dir)
                dst_file = self.target_dir / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
                copied_count += 1
                
                # Update progress every 50 files
                if copied_count % 50 == 0:
                    pct = 50 + int((copied_count / total_files) * 40)
                    self.progress.emit(pct)
                    self._log_status(f"   Copying: {copied_count}/{total_files} files...")
            
            # Also copy JSON files
            for json_file in source_dir.glob('*.json'):
                shutil.copy2(json_file, self.target_dir / json_file.name)
            
            self._log_status(f"🧹 Cleaning up temporary files...")
            self.progress.emit(95)
            
            # Clean up temp dir (with Windows-safe cleanup)
            try:
                # First, remove .git folder which has locked files
                git_dir = temp_dir / ".git"
                if git_dir.exists():
                    shutil.rmtree(git_dir, onerror=self._remove_readonly)
                # Then remove the rest
                shutil.rmtree(temp_dir, onerror=self._remove_readonly)
            except Exception as e:
                self._log_status(f"   Note: Temp cleanup had issues (safe to ignore): {e}")
            
            self._log_status(f"✅ Successfully downloaded {copied_count} samples for {display_name}!")
            self.progress.emit(100)
            self.finished.emit(True)
            
        except subprocess.TimeoutExpired:
            self._log_status("❌ Download timed out (10 minutes)")
            self.finished.emit(False)
        except Exception as e:
            logger.error(f"Sample download error: {e}")
            self._log_status(f"❌ Error: {e}")
            self.finished.emit(False)

