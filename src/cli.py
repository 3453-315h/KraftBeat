#!/usr/bin/env python
"""
Kraftbeat CLI - Command-line music generation

Usage:
    python -m src.cli "epic orchestral battle music" -d 30 -o battle.wav
    python -m src.cli --help
"""

import argparse
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Kraftbeat CLI - AI Text-to-Music Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.cli "ambient electronic chill" -d 15 -o chill.wav
  python -m src.cli "epic orchestral" --model large --duration 30
  python -m src.cli "funky bass groove" -f mp3 --bpm 120 --key "C Minor"
        """
    )
    
    # Required
    parser.add_argument("prompt", help="Text description of the music to generate")
    
    # Output
    parser.add_argument("-o", "--output", default="output.wav",
                        help="Output file path (default: output.wav)")
    parser.add_argument("-f", "--format", choices=["wav", "mp3", "flac", "ogg"],
                        default="wav", help="Output format (default: wav)")
    parser.add_argument("--bitrate", default="192k",
                        help="Bitrate for MP3/OGG (default: 192k)")
    
    # Generation
    parser.add_argument("-d", "--duration", type=int, default=10,
                        help="Duration in seconds (default: 10)")
    parser.add_argument("-t", "--temperature", type=float, default=1.0,
                        help="Generation temperature 0.1-2.0 (default: 1.0)")
    parser.add_argument("-m", "--model", default="small",
                        choices=["small", "medium", "melody", "large"],
                        help="Model size (default: small)")
    
    # Music controls
    parser.add_argument("--bpm", type=int, help="Target BPM (20-300)")
    parser.add_argument("--key", help="Musical key (e.g., 'C Major', 'A Minor')")
    parser.add_argument("--loop", action="store_true",
                        help="Generate seamless loop")
    
    # Effects
    parser.add_argument("--reverb", type=int, default=0,
                        help="Reverb amount 0-100 (default: 0)")
    parser.add_argument("--compress", type=int, default=0,
                        help="Compression amount 0-100 (default: 0)")
    parser.add_argument("--bass", type=int, default=0,
                        help="Bass EQ -12 to +12 dB (default: 0)")
    parser.add_argument("--treble", type=int, default=0,
                        help="Treble EQ -12 to +12 dB (default: 0)")
    
    # System
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")
    parser.add_argument("--device", choices=["auto", "cuda", "directml", "mps", "cpu"],
                        default="auto", help="Compute device (default: auto)")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Build full prompt with modifiers
    prompt = args.prompt
    if args.bpm:
        prompt += f", {args.bpm} BPM"
    if args.key:
        prompt += f", {args.key}"
    if args.loop:
        prompt += ", seamless loop"
    
    logger.info(f"🎵 Kraftbeat CLI")
    logger.info(f"   Prompt: {prompt}")
    logger.info(f"   Duration: {args.duration}s")
    logger.info(f"   Model: {args.model}")
    logger.info(f"   Output: {args.output}")
    
    try:
        # Import here to avoid slow startup for --help
        from src.device import get_device
        from src.models.musicgen import MusicGenLoader
        from src.utils.audio import save_audio, normalize_audio
        
        # Determine device
        device_str = args.device
        preferred_device = None
        if device_str != "auto":
            from src.device import DeviceType
            try:
                preferred_device = DeviceType(device_str)
            except ValueError:
                pass # Fallback to auto if invalid
        
        device_info = get_device(preferred_device)
        
             
        logger.info(f"🖥️ Device: {device_info.device_name} ({device_info.device_type.value})")

        # Load model
        logger.info(f"⏳ Loading model...")
        loader = MusicGenLoader(device_info)
        
        # Load model using short key (e.g. "small")
        if not loader.load_model(args.model):
            logger.error(f"❌ Failed to load model: {args.model}")
            sys.exit(1)
            
        logger.info(f"✅ Model loaded: {args.model}")
        
        # Generate
        logger.info(f"🎹 Generating...")
        audio = loader.generate(
            prompt=prompt,
            duration=args.duration,
            temperature=args.temperature,
        )
        logger.info(f"✅ Generated {args.duration}s of audio")
        
        # Apply effects if any
        if args.reverb > 0 or args.compress > 0 or args.bass != 0 or args.treble != 0:
            logger.info(f"🎛️ Applying effects...")
            try:
                from src.utils.effects import apply_effects_chain
                audio = apply_effects_chain(
                    audio,
                    loader.sample_rate,
                    reverb_wet=args.reverb / 100.0,
                    compression_ratio=1.0 + (args.compress / 25.0),
                    eq_bass=float(args.bass),
                    eq_treble=float(args.treble),
                )
            except Exception as e:
                logger.warning(f"Effects failed: {e}")
        
        # Normalize and save
        audio = normalize_audio(audio)
        output_path = Path(args.output)
        if output_path.suffix.lower()[1:] != args.format:
            output_path = output_path.with_suffix(f".{args.format}")
        
        success = save_audio(
            audio,
            str(output_path),
            loader.sample_rate,
            args.format,
            args.bitrate
        )
        
        if success:
            logger.info(f"💾 Saved: {output_path}")
            logger.info(f"🎉 Done!")
        else:
            logger.error(f"❌ Failed to save audio")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\n⏹️ Cancelled")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
