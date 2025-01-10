# Example usage
import Pycamo as pycamo
# get color from image
color_palette = pycamo.extract_palette("demo_input/teste3.png", num_colors=4)

# custom color palette
#color_palette = ['0d011c', '1D1107', '011c07', '012e04']

#pixelize
pixelize = True # Set to True to pixelize the output image 
pixel_size =  3# Size of the pixelization

# Ratios for each color in the palette
ratios = [25, 25, 25, 25]  # Example ratios for each color

pycamo.generate_pattern(color_palette, "gencamo.png", size=(500, 500), c=1.2, ratios=ratios, pixelize=pixelize)