import warnings
warnings.filterwarnings('ignore')
import numpy as np
from PIL import Image
from skimage.filters.rank import modal
import Colorpg as cp

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


def generate_pattern(colors_hex, output_filename, size=(), c=2.0, ratios=None):
    fp = np.ones((3, 3)).astype(np.uint8)

    
    rgb_colors = [hex2rgb(c.strip()) for c in colors_hex]
    palette = []
    for cc, hex in zip(rgb_colors, colors_hex):
        palette += cc

    n_colors = len(colors_hex)

    
    if ratios is None:
        ratios = [1 / n_colors] * n_colors  # Equal ratio by default
    else:
        assert len(ratios) == n_colors, "Make sure the number of ratios matches the number of colors"
        assert np.isclose(sum(ratios), 100), "Ratios must sum to 100%"
        ratios = np.array(ratios) / sum(ratios)  # Normalize ratios to sum to 1

    # Generate initial random noise layers
    layers = np.array([nat_filt_im(size=size, c=c) * r for r in ratios])

    # Combine layers by selecting the highest value at each pixel
    combined_map = np.argmax(layers, axis=0)

    # Apply modal filter for smoothing
    final_map = modal(combined_map.astype(np.uint8), fp)

    img = Image.new("P", size, (0, 0, 0))
    img.putdata(final_map.flatten())
    img.putpalette(palette)
    img.save(output_filename)
    return img

# Example usage
# get color from image
color_palette = cp.extract_palette("demo_input/teste3.png", num_colors=4)
# custom color palette
#color_palette = ['0d011c', '1D1107', '011c07', '012e04']
ratios = [25, 25, 25, 25]  # Example ratios for each color
generate_pattern(color_palette, "gencamo.png", size=(1024, 1024), c=1.2, ratios=ratios)
