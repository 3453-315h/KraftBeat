import sys
import os
import time
from pathlib import Path
import logging

try:
    # Add src to path to import local modules
    sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
    from models.catalog import MODEL_CATALOG
    from device import DeviceInfo, DeviceType
except ImportError as e:
    print(f"Error importing Kraftbeat modules: {e}")
    sys.exit(1)

# Configure simplified logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("ModelDownloader")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║  Kraftbeat Model Downloader                                ║")
    print("╠════════════════════════════════════════════════════════════╣")

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"

def main():
    # Helper loaders (lazy init)
    loaders = {}
    
    def get_loader(family):
        if family not in loaders:
            if family in ['MusicGen', 'AudioGen', 'MAGNeT']:
                from models.musicgen import MusicGenLoader
                loaders[family] = MusicGenLoader(None)
            elif family == 'ACESTEP':
                from models.ace_step import ACEStepLoader
                loaders[family] = ACEStepLoader()
            elif family == 'DIFFRHYTHM':
                from models.diffrhythm import DiffRhythmLoader
                loaders[family] = DiffRhythmLoader()
        return loaders.get(family)

    while True:
        clear_screen()
        print_header()
        
        # List available models from shared catalog
        models = list(MODEL_CATALOG.keys())
        
        print(f"{'  #':<4} {'Name':<28} {'Size':<10} {'VRAM':<8} {'Desc'}")
        print("────────────────────────────────────────────────────────────────────────")
        
        for i, key in enumerate(models):
            info = MODEL_CATALOG[key]
            size_str = info['download_size']
            vram_str = f"{info['vram_gb']}GB"
            desc = info['description'][:35] + "..." if len(info['description']) > 35 else info['description']
            
            print(f"  {i+1:<3} {info['display_name']:<28} {size_str:<10} {vram_str:<8} {desc}")
            
        print("\n  [A] Download ALL  [Q] Quit")
        print("────────────────────────────────────────────────────────────────────────")
        
        choice = input("\n  Enter selection #: ").strip().lower()
        
        if choice == 'q':
            break
            
        if choice == 'a':
            print("\n  Starting download of ALL models...")
            for key in models:
                info = MODEL_CATALOG[key]
                family = info['family']
                loader = get_loader(family)
                if loader:
                    print(f"  > Downloading {info['display_name']}...")
                    loader.download_model(key)
                else:
                    print(f"  [ERROR] No loader for {family}")
            input("\n  All downloads finished. Press Enter.")
            continue
            
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(models):
                target_model = models[idx]
                info = MODEL_CATALOG[target_model]
                family = info['family']
                
                print(f"\n  > Starting download for: {info['display_name']}")
                print(f"  > Family: {family}")
                print("  > This may take a while depending on your internet connection.")
                print("  > DO NOT CLOSE THIS WINDOW.\n")
                
                loader = get_loader(family)
                if loader:
                    success = loader.download_model(target_model)
                    
                    if success:
                        print(f"\n  ✅ Successfully downloaded {target_model}!")
                    else:
                        print(f"\n  ❌ Failed to download {target_model}. Check logs/internet.")
                else:
                    print(f"\n  ❌ Error: Could not initialize loader for {family}")
                
                input("\n  Press Enter to continue...")
            else:
                input("\n  Invalid number. Press Enter.")
        else:
            input("\n  Invalid selection. Press Enter.")

if __name__ == "__main__":
    main()
