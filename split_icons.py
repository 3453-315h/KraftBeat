
"""
Script to split the generated icon sheet into individual PNG files.
Requires: pip install pillow
"""

import os
from PIL import Image

def split_icons(image_path, output_dir):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    
    # Grid configuration (3 rows, 4 columns based on prompt)
    cols = 3
    rows = 4
    
    # Calculate cell size
    cell_w = width // cols
    cell_h = height // rows
    
    # Icon names in order (left to right, top to bottom)
    icon_names = [
        "home.png", "generate.png", "play.png",
        "stop.png", "save.png", "folder.png",
        "project.png", "stems.png", "cache.png",
        "mic.png", "theme.png", "settings.png"
    ]
    
    print(f"Splitting {width}x{height} image into {rows}x{cols} grid...")
    
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= len(icon_names):
                break
                
            left = c * cell_w
            top = r * cell_h
            right = left + cell_w
            bottom = top + cell_h
            
            # Crop
            icon = img.crop((left, top, right, bottom))
            
            # Smart crop - find bounding box of content (non-black/transparent)
            # Since background is black, we make black transparent first
            datas = icon.getdata()
            new_data = []
            for item in datas:
                # If pixel is black (or very close to it), make it transparent
                if item[0] < 30 and item[1] < 30 and item[2] < 30:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            icon.putdata(new_data)
            
            # Now crop to content
            bbox = icon.getbbox()
            if bbox:
                icon = icon.crop(bbox)
                
            # Resize standard size (ensure square canvas)
            target_size = 64
            final_icon = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
            
            # Paste centered
            offset = ((target_size - icon.width) // 2, (target_size - icon.height) // 2)
            final_icon.paste(icon, offset)
            
            # Save
            out_path = os.path.join(output_dir, icon_names[idx])
            final_icon.save(out_path, "PNG")
            print(f"Saved {out_path}")
            
            idx += 1

if __name__ == "__main__":
    # Replace this with the actual path to the generated image artifact
    # Since I cannot see the artifact path in this context, I will assume a standard location 
    # or the user will move it. 
    # For now, I'll set a placeholder path.
    generated_image_path = "kraftbeat_icons.png" 
    output_directory = "src/ui/assets/icons"
    
    # Check if PIL is installed
    try:
        import PIL
        print("Pillow installed, proceeding...")
        if os.path.exists(generated_image_path):
             split_icons(generated_image_path, output_directory)
        else:
            print(f"Please place the generated 'kraftbeat_icons.png' in the project root.")
    except ImportError:
        print("Pillow not installed. Run: pip install pillow")
