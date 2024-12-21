import warnings
warnings.filterwarnings('ignore')
import numpy as np
from PIL import Image
from skimage.filters.rank import modal
import Colorpg as cp

def hex2rgb(hex: str):
  return [int(hex[i:i+2], 16) for i in (0, 2, 4)]

def nat_filt_im(size=(), c=2.0):
    width, height = size
    x = np.linspace(-1, 1, width)
    y = np.linspace(-1, 1, height)
    X, Y = np.meshgrid(x, y)
    
    # Calculate scaled distances
    wdist = np.abs(X)
    hdist = np.abs(Y)
    
    # Create distance matrix normalized to image dimensions
    cdist = np.sqrt(wdist**2 + hdist**2)
    cdist = cdist / np.max(cdist)  # Normalize to [0,1]
    
    # Apply power law filter
    filter = 1.0/(cdist + 1e-6)**c
    
    # Generate and filter random image
    rand_im = np.random.random((height, width))
    rand_im_fourier = np.fft.fftshift(np.fft.fft2(rand_im))
    filtered = np.real(np.fft.ifft2(np.fft.ifftshift(rand_im_fourier * filter)))
    
    return filtered
c= 1.5
def generate_pattern(colors_hex, output_filename, size=()):
    fp = np.ones((3, 3)).astype(np.uint8)
    
    rgb_colors = [hex2rgb(c.strip()) for c in colors_hex]
    palette = []
    for cc, hex in zip(rgb_colors, colors_hex):
        palette += cc

    n_colors = len(colors_hex)
    props = np.ones(n_colors)

    fims = np.stack([p*nat_filt_im(size=size, c=c) for p, _ in zip(props, range(n_colors))], axis=-1)
    xf = np.argmax(fims, axis=2)
    xf = modal(xf, fp)
    img = Image.new("P", size, (0,0,0))
    img.putdata(xf.astype(np.uint8).flatten())
    img.putpalette(palette)
    img.save(output_filename)
    return img

# Example usage:                    replace image path with your own
color_palette = cp.extract_palette("demo_input/testimg2.jpg", num_colors=4)
generate_pattern(color_palette, "gencamo.png", size=(500, 500))
#                            output image name     custom size