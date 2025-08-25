from PIL import Image
import os
import re

input_folder = './images'
output_folder = './battery_icons_colored'
os.makedirs(output_folder, exist_ok=True)

# Gradient colors: red → yellow → green
color_red = (255, 0, 0)
color_yellow = (255, 255, 0)
color_green = (0, 255, 0)

def interpolate_color(start, end, t):
    """Linear interpolation between two colors."""
    return tuple(int(s + (e - s) * t) for s, e in zip(start, end))

def fill_level_to_color(level_percent):
    """Convert fill level (0–100) to gradient color."""
    t = level_percent / 100
    if t < 0.5:
        return interpolate_color(color_red, color_yellow, t / 0.5)
    else:
        return interpolate_color(color_yellow, color_green, (t - 0.5) / 0.5)

for filename in os.listdir(input_folder):
    if filename.endswith('.png'):
        img = Image.open(os.path.join(input_folder, filename)).convert('RGBA')

        # Extract battery percentage from filename
        match = re.search(r'(\d+)', filename)
        if match:
            level = int(match.group(1))
        else:
            level = 100  # default if no number found

        color = fill_level_to_color(level)

        # Apply color while keeping transparency
        new_data = [
            (*color, px[3]) if px[3] > 0 else px
            for px in img.getdata()
        ]
        img.putdata(new_data)
        img.save(os.path.join(output_folder, filename))

print("All battery icons recolored based on filename percentage!")
