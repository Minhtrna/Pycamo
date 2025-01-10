# Example usage
import Pycamo as pycamo
# get color from image
color_palette = pycamo.extract_palette("demo_input/teste3.png", num_colors=4)

# custom color palette
#color_palette = ['0d011c', '1D1107', '011c07', '012e04']

pixelize = False # Set to True to pixelize the output image 

ratios = [25, 25, 25, 25]  # Example ratios for each color

pycamo.generate_pattern(color_palette, "gencamo.png", size=(1024, 1024), c=1.2, ratios=ratios, pixelize=pixelize)