from PIL import Image, ImageDraw, ImageFont
import os
import glob

def generate_icon(pack_path, output_path):
    # Try to find existing icon candidates
    candidates = [
        *glob.glob(os.path.join(pack_path, "**/*.png"), recursive=True),
        *glob.glob(os.path.join(pack_path, "**/logo.*"), recursive=True),
        *glob.glob(os.path.join(pack_path, "**/icon.*"), recursive=True)
    ]
    
    # Try to use first candidate image
    for candidate in candidates:
        try:
            img = Image.open(candidate)
            return process_image(img, output_path)
        except:
            continue
    
    # Fallback to generated icon
    create_text_icon("Pack Icon", output_path)

def process_image(img, output_path, size=64):
    # Crop to square aspect ratio
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim)/2
    top = (height - min_dim)/2
    right = (width + min_dim)/2
    bottom = (height + min_dim)/2
    
    img = img.crop((left, top, right, bottom))
    img = img.resize((size, size))
    img.save(output_path)
    return True

def create_text_icon(text, output_path, size=64):
    img = Image.new("RGB", (size, size), "#4B6A87")
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text(
        (size/2, size/2), 
        text, 
        font=font,
        anchor="mm",
        fill="#FFFFFF"
    )
    
    img.save(output_path)
