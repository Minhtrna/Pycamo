import warnings
warnings.filterwarnings('ignore')
import numpy as np
from PIL import Image
from skimage.filters.rank import modal

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
    return hex_colors

# Convert hex color to RGB
def hex2rgb(hex: str):
    return [int(hex[i:i+2], 16) for i in (0, 2, 4)]

# Generate filtered noise image
def nat_filt_im(size=(), c=2.0):
    width, height = size
    x = np.linspace(-1, 1, width)
    y = np.linspace(-1, 1, height)
    X, Y = np.meshgrid(x, y)

    
    wdist = np.abs(X)
    hdist = np.abs(Y)

    # Create distance matrix normalized to image dimensions
    cdist = np.sqrt(wdist**2 + hdist**2)
    cdist = cdist / np.max(cdist)  # Normalize to [0,1]

    # Apply power law filter
    filter = 1.0 / (cdist + 1e-6)**c

    # Generate and filter random image
    rand_im = np.random.random((height, width))
    rand_im_fourier = np.fft.fftshift(np.fft.fft2(rand_im))
    filtered = np.real(np.fft.ifft2(np.fft.ifftshift(rand_im_fourier * filter)))

    # Normalize filtered output to [0, 1]
    filtered = (filtered - np.min(filtered)) / (np.max(filtered) - np.min(filtered))

    return filtered

def pixelize_image(image, pixel_size=10):
    # Load the image
    image = image
    # Resize the image to a smaller size
    small_image = image.resize(
        (image.width // pixel_size, image.height // pixel_size), Image.NEAREST)
    # Resize back to the original size
    pixelated_image = small_image.resize(image.size, Image.NEAREST)
    return pixelated_image

def generate_pattern(colors_hex, output_filename, size=(), c=2.0, ratios=None, pixelize=False):
    fp = np.ones((3, 3)).astype(np.uint8)
    
    # Filter out colors with zero ratios 
    if ratios is not None:
        non_zero_indices = [i for i, r in enumerate(ratios) if r > 0]
        colors_hex = [colors_hex[i] for i in non_zero_indices]
        ratios = [ratios[i] for i in non_zero_indices]
    
    rgb_colors = [hex2rgb(c.strip()) for c in colors_hex]
    palette = []
    for cc, hex in zip(rgb_colors, colors_hex):
        palette += cc

    n_colors = len(colors_hex)
    
    if ratios is None:
        ratios = [1 / n_colors] * n_colors
    else:
        assert len(ratios) == n_colors
        assert np.isclose(sum(ratios), 100)
        ratios = np.array(ratios) / sum(ratios)

    # Generate separate noise layers only for non-zero colors
    noise_layers = [nat_filt_im(size=size, c=c) for _ in range(n_colors)]
    
    total_pixels = size[0] * size[1]
    pixel_counts = np.round(ratios * total_pixels).astype(int)
    pixel_counts[-1] = total_pixels - np.sum(pixel_counts[:-1])
    
    # Create color map
    color_map = np.zeros(total_pixels, dtype=np.uint8)
    
    # Process each layer
    remaining_indices = set(range(total_pixels))
    for i, layer in enumerate(noise_layers):
        if i == n_colors - 1:
            indices = list(remaining_indices)
        else:
            flat_layer = layer.flatten()
            sorted_indices = np.argsort(flat_layer)
            valid_indices = [idx for idx in sorted_indices if idx in remaining_indices]
            indices = valid_indices[-pixel_counts[i]:]
            
        remaining_indices -= set(indices)
        color_map[indices] = i

    color_map = color_map.reshape(size)
    final_map = modal(color_map, fp)

    img = Image.new("P", size, (0, 0, 0))
    img.putdata(final_map.flatten())
    img.putpalette(palette)
    if pixelize is True:
        img = pixelize_image(img, pixel_size=10)
        img.save(output_filename)
    else:
        img.save(output_filename)
    return img

# Example usage
# get color from image
#pixelize = True # Set to True to pixelize the output image 
#color_palette = extract_palette("demo_input/teste3.png", num_colors=4)
# custom color palette
#color_palette = ['0d011c', '1D1107', '011c07', '012e04']
#ratios = [25, 25, 25, 25]  # Example ratios for each color
#generate_pattern(color_palette, "gencamo.png", size=(1024, 1024), c=1.2, ratios=ratios, pixelize=pixelize)
