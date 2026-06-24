from PIL import Image
from pathlib import Path
import os

def split_splash_image():
    source_path = Path("Gemini_Generated_Image_71u4vd71u4vd71u4.png")
    output_dir = Path("src/ui/assets/splash")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not source_path.exists():
        print(f"Error: {source_path} not found.")
        return

    img = Image.open(source_path)
    width, height = img.size
    print(f"Source image size: {width}x{height}")
    
    # 2x2 grid
    w = width // 2
    h = height // 2
    
    quadrants = [
        (0, 0, w, h),       # Top-Left
        (w, 0, width, h),   # Top-Right
        (0, h, w, height),  # Bottom-Left
        (w, h, width, height) # Bottom-Right
    ]
    
    for i, box in enumerate(quadrants):
        crop = img.crop(box)
        out_path = output_dir / f"splash_{i+1}.png"
        crop.save(out_path)
        print(f"Saved {out_path} ({w}x{h})")

if __name__ == "__main__":
    split_splash_image()
