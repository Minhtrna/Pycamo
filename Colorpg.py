import numpy as np
from PIL import Image

def median_cut(pixels, num_colors):
    boxes = [np.array(pixels)]
    while len(boxes) < num_colors:
        widest_box_index = np.argmax([
            np.ptp(box, axis=0).max() for box in boxes
        ])
        widest_box = boxes.pop(widest_box_index)
        dominant_dim = np.ptp(widest_box, axis=0).argmax()
        sorted_box = widest_box[np.argsort(widest_box[:, dominant_dim])]
        median_index = len(sorted_box) // 2
        boxes.append(sorted_box[:median_index])
        boxes.append(sorted_box[median_index:])
    return boxes

def get_palette(boxes):
    return [tuple(map(int, np.mean(box, axis=0))) for box in boxes]

def convert_palette_to_hex(palette):
    return [f"{r:02x}{g:02x}{b:02x}" for r, g, b in palette]

def extract_palette(image_path, num_colors=5):
    image = Image.open(image_path).convert("RGB")
    image = image.resize((500, 500))
    # Convert to pixels
    pixels = np.array(list(image.getdata()))
    # Process
    boxes = median_cut(pixels, num_colors)
    palette = get_palette(boxes)
    hex_colors = convert_palette_to_hex(palette)
    print(hex_colors)
    return hex_colors

