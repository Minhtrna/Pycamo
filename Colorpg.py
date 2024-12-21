import numpy as np
from PIL import Image

def median_cut(pixels, num_colors):
    """Split pixels into boxes using median cut algorithm
    Args:
        pixels (np.array): Array of RGB pixels
        num_colors (int): Number of colors to extract
    Returns:
        list: List of pixel boxes
    """
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
    """Average colors in boxes to create palette
    Args:
        boxes (list): List of pixel boxes
    Returns:
        list: List of RGB tuples
    """
    return [tuple(map(int, np.mean(box, axis=0))) for box in boxes]

def convert_palette_to_hex(palette):
    """Convert RGB tuples to hex codes
    Args:
        palette (list): List of RGB tuples
    Returns:
        list: List of hex color codes
    """
    return [f"{r:02x}{g:02x}{b:02x}" for r, g, b in palette]

def extract_palette(image_path, num_colors=5):
    """Extract color palette from image
    Args:
        image_path (str): Path to input image
        num_colors (int): Number of colors to extract (default: 5)
    Returns:
        list: List of hex color codes
    """
    try:
        # Load and resize image
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
    except Exception as e:
        raise Exception(f"Failed to process image: {str(e)}")

