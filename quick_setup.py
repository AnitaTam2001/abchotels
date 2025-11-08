# quick_setup.py - Simple script to create all required files
import os
from PIL import Image, ImageDraw

def quick_image_setup():
    """Quick setup to create all required room images"""
    
    image_dir = "static/images/rooms"
    os.makedirs(image_dir, exist_ok=True)
    
    room_types = [
        "accessible_king", "junior_suite", "poolview_king", "cityview_twin",
        "corner_suite", "studio_king", "connecting_family", "garden_queen", 
        "extended_stay", "penthouse_suite"
    ]
    
    colors = [
        (173, 216, 230), (144, 238, 144), (135, 206, 250), (192, 192, 192),
        (255, 218, 185), (221, 160, 221), (255, 228, 196), (152, 251, 152),
        (176, 224, 230), (255, 250, 205)
    ]
    
    print("Creating room images...")
    
    for i, room_type in enumerate(room_types):
        filename = f"{image_dir}/{room_type}.jpg"
        
        # Create colored image with label
        img = Image.new('RGB', (800, 600), color=colors[i])
        draw = ImageDraw.Draw(img)
        
        # Add room name
        room_name = room_type.replace('_', ' ').title()
        draw.text((400, 300), room_name, fill=(0, 0, 0), anchor="mm")
        
        img.save(filename, "JPEG", quality=95)
        print(f"✓ Created {room_type}.jpg")
    
    print(f"\n✅ All 10 room images created in: {image_dir}/")

if __name__ == "__main__":
    quick_image_setup()