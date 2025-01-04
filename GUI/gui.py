# This GUI generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

import os
from pathlib import Path
import ctypes
import numpy as np
from PIL import Image, ImageTk
import warnings
warnings.filterwarnings('ignore')
from skimage.filters.rank import modal
from tkinter import messagebox
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

# path

OUTPUT_PATH = Path(__file__).parent.resolve()
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
###################### Color extraction ######################
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
###################### Camogen ######################
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
        assert len(ratios) == n_colors,  messagebox.showerror("Error", "Please fill color precentages")
        assert np.isclose(sum(ratios), 100), messagebox.showerror("Error", "Sum of color precentages should be 100")
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
####### Load image #######
# Load image in to Input image canvas when button_1 is clicked file explorer window should be open to select the image.
loaded_image = None

def load_image():
    global loaded_image
    # Open file explorer window to select the image
    from tkinter import filedialog
    file_path = filedialog.askopenfilename()
    # display the image in the Input image canvas
    img = Image.open(file_path)
    img = img.resize((200, 200), Image.LANCZOS)
    loaded_image = ImageTk.PhotoImage(img)
    canvas.create_image(138.0, 229.0, image=loaded_image)
    canvas.image = loaded_image
    # Extract color palette, use number of colors extracted as the number of colors in entry_Numcolor if it is empty use 5 as default.
    if entry_Numcolor.get() == "":
        num_colors = 5
    else:
        num_colors = int(entry_Numcolor.get())
    colors_hex = extract_palette(file_path, num_colors)
    # fill the extracted colors in the color entry boxes.
    for i, color in enumerate(colors_hex):
        entry = eval(f"entry_Cl{i+1}")
        entry.delete(0, "end")
        entry.insert(0, color)

def generate_pattern_from_entries():
    # Collect colors from entry boxes, ignoring blank entries
    colors_hex = [entry_Cl1.get(), entry_Cl2.get(), entry_Cl3.get(), entry_Cl4.get(), entry_Cl5.get()]
    colors_hex = [color for color in colors_hex if color]  # Filter out empty color entries
    
    # Collect ratios from entry boxes
    ratios = [entry_p1.get(), entry_p2.get(), entry_p3.get(), entry_p4.get(), entry_p5.get()]
    ratios = [float(r) for r in ratios if r]  # Filter out empty ratio entries
    if "" in ratios:
        ratios = None
    else:
        ratios = [float(r) for r in ratios]
    
    # Default value for entry_Cvalue if empty
    if entry_Cvalue.get() == "":
        entry_Cvalue.insert(0, "1.2")
    # check if the camo size entry boxes are empty if empty show error message.
    if entry_size1.get() == "" or entry_size2.get() == "":
        messagebox.showerror("Error", "Please fill camo size")
    # Generate the pattern
    output_file = os.path.join(OUTPUT_PATH, "Camo.png")
    generate_pattern(colors_hex, output_file, (int(entry_size1.get()), int(entry_size2.get())), c=float(entry_Cvalue.get()), ratios=ratios)
    
    # Display the generated pattern in the preview canvas
    img = Image.open(output_file)
    img = img.resize((500, 500), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(956.0, 347.0, image=img)
    canvas.image = img
# Show output image folder when button_2 is clicked
def show_output_folder():
    import os
    os.system("start %s" % OUTPUT_PATH)
# Create the GUI
window = Tk()
window.geometry("1280x720")
window.configure(bg = "#1E2124")
canvas = Canvas(window,bg = "#1E2124",height = 720,width = 1280,bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)
###### preview text ######
canvas.create_text(730.0,28.0,anchor="nw",text="Preview ( Preview window size is 500x500 )",fill="#FFFFFF",font=("Inter", 24 * -1))
###### parameter text ######
canvas.create_text(96.0,28.0,anchor="nw",text="Parameter",fill="#FFFFFF",font=("Inter", 24 * -1))
###### input image canvas ######
canvas.create_rectangle(10.0,79.0,666.0,653.0,fill="#1E2124",outline="")
###### ??? ###### :))) auto gen by tkinter designer
canvas.create_rectangle(15.0,86.0,662.0,649.0,fill="#444B53",outline="")
###### preview canvas ######
canvas.create_rectangle(706.0,97.0,1206.0,597.0,fill="#D9D9D9",outline="")
###### open image button ######
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=lambda: load_image(),relief="flat")
button_1.place(x=316.0,y=91.0,width=212.0,height=67.0)
###### preview canvas ######
canvas.create_text(38.0,97.0,anchor="nw",text="Input image",fill="#FFFFFF",font=("Inter", 24 * -1))
canvas.create_rectangle(38.0,129.0,238.0,329.0,fill="#1E2124",outline="")
###### save camo button ######
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2,borderwidth=0,highlightthickness=0,command=lambda: show_output_folder(),relief="flat")
button_2.place(x=437.0,y=287.0,width=182.0,height=42.0)
###### generate camo button ######
button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=button_image_3,borderwidth=0,highlightthickness=0,command=lambda: generate_pattern_from_entries(),relief="flat")
button_3.place(x=246.0,y=287.0,width=183.0,height=42.0)
###### parameter canvas ######
canvas.create_rectangle(38.0,342.0,438.0,597.0,fill="#FCFCFC",outline="")
canvas.create_rectangle(454.0,342.0,652.0,597.0,fill="#FCFCFC",outline="")

############## C value entry box ##############
entry_image_Cvalue = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_Cvalue = canvas.create_image(553.0,387.0,image=entry_image_Cvalue)
entry_Cvalue = Entry(bd=0,bg="#D1D8DE",fg="#000716",highlightthickness=0)
entry_Cvalue.place(x=466.0,y=372.0,width=174.0,height=28.0)

############## Number of colors entry box ##############
entry_image_Numcolor = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_Numcolor = canvas.create_image(336.0,188.0,image=entry_image_Numcolor)
entry_Numcolor = Entry(bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
entry_Numcolor.place(x=249.0,y=173.0,width=174.0,height=28.0)

# Group Cl: Color entries
entry_image_Cl1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(137.0, 384.0, image=entry_image_Cl1)
entry_Cl1 = Entry(bd=0, bg="#D1D8DE", fg="#000716", highlightthickness=0)
entry_Cl1.place(x=50.0, y=369.0, width=174.0, height=28.0)

entry_image_Cl2 = PhotoImage(file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(137.0, 432.0, image=entry_image_Cl2)
entry_Cl2 = Entry(bd=0, bg="#D1D8DE", fg="#000716", highlightthickness=0)
entry_Cl2.place(x=50.0, y=417.0, width=174.0, height=28.0)

entry_image_Cl3 = PhotoImage(file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(137.0, 480.0, image=entry_image_Cl3)
entry_Cl3 = Entry(bd=0, bg="#D1D8DE", fg="#000716", highlightthickness=0)
entry_Cl3.place(x=50.0, y=465.0, width=174.0, height=28.0)

entry_image_Cl4 = PhotoImage(file=relative_to_assets("entry_9.png"))
entry_bg_9 = canvas.create_image(137.0, 528.0, image=entry_image_Cl4)
entry_Cl4 = Entry(bd=0, bg="#D1D8DE", fg="#000716", highlightthickness=0)
entry_Cl4.place(x=50.0, y=513.0, width=174.0, height=28.0)

entry_image_Cl5 = PhotoImage(file=relative_to_assets("entry_11.png"))
entry_bg_11 = canvas.create_image(139.0, 576.0, image=entry_image_Cl5)
entry_Cl5 = Entry(bd=0, bg="#D1D8DE", fg="#000716", highlightthickness=0)
entry_Cl5.place(x=52.0, y=561.0, width=174.0, height=28.0)

# Group P: Percent entries
entry_image_p1 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_precent1 = canvas.create_image(373.0, 383.0, image=entry_image_p1)
entry_p1 = Entry(bd=0, bg="#D1D8DE", fg="#000716", highlightthickness=0)
entry_p1.place(x=338.0, y=368.0, width=70.0, height=28.0)

entry_image_p2 = PhotoImage(file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(373.0, 431.0, image=entry_image_p2)
entry_p2 = Entry(bd=0, bg="#D1D8DE", fg="#000716", highlightthickness=0)
entry_p2.place(x=338.0, y=416.0, width=70.0, height=28.0)

entry_image_p3 = PhotoImage(file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(373.0, 479.0, image=entry_image_p3)
entry_p3 = Entry(bd=0, bg="#D1D8DE", fg="#000716", highlightthickness=0)
entry_p3.place(x=338.0, y=464.0, width=70.0, height=28.0)

entry_image_p4 = PhotoImage(file=relative_to_assets("entry_10.png"))
entry_bg_10 = canvas.create_image(373.0, 527.0, image=entry_image_p4)
entry_p4 = Entry(bd=0, bg="#D1D8DE", fg="#000716", highlightthickness=0)
entry_p4.place(x=338.0, y=512.0, width=70.0, height=28.0)

entry_image_p5 = PhotoImage(file=relative_to_assets("entry_12.png"))
entry_bg_12 = canvas.create_image(374.0, 575.0, image=entry_image_p5)
entry_p5 = Entry(bd=0, bg="#D1D8DE", fg="#000716", highlightthickness=0)
entry_p5.place(x=338.0, y=560.0, width=72.0, height=28.0)
# create 2 entry boxes for camo size 
entry_size1 = Entry( bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_size2 = Entry( bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_size1.place( x=440.0, y=220.0, width=74.0, height=28.0)
entry_size2.place( x=336.0, y=220.0, width=74.0, height=28.0)
canvas.create_text( 418.0, 220.0, anchor="nw", text="x", fill="#FFFFFF", font=("Inter", 24 * -1))
canvas.create_text( 370.0, 250.0, anchor="nw", text="Camo size", fill="#FFFFFF", font=("Inter", 24 * -1))
###################### Parameter names ######################
canvas.create_text(52.0,342.0,anchor="nw",text="Color",fill="#000000",font=("Inter", 24 * -1))

canvas.create_text(322.0,341.0,anchor="nw",text="Percent",fill="#000000",font=("Inter", 24 * -1))

canvas.create_text(438.0,173.0,anchor="nw",text="Color extract",fill="#FFFFFF",font=("Inter", 24 * -1))

canvas.create_text(470.0,342.0,anchor="nw",text="C vaule",fill="#000000",font=("Inter", 24 * -1))

canvas.create_text(466.0,409.0,anchor="nw",
    text="""    C value will 
    affect the result. 
    Look github repo 
    for more information""",fill="#000000",font=("Inter", 16 * -1))

# Update color preview rectangles every 100ms
def update_colors():
    fills = []
    for entry in [entry_Cl1, entry_Cl2, entry_Cl3, entry_Cl4, entry_Cl5]:
        color = entry.get()
        if len(color) == 6 and all(c in '0123456789ABCDEFabcdef' for c in color):
            fills.append("#" + color)
        else:
            fills.append("#000000")
    
    canvas.itemconfig(rect1, fill=fills[0])
    canvas.itemconfig(rect2, fill=fills[1])
    canvas.itemconfig(rect3, fill=fills[2])
    canvas.itemconfig(rect4, fill=fills[3])
    canvas.itemconfig(rect5, fill=fills[4])
    
    window.after(100, update_colors)

# Create 5 small rectangles to show the color extracted from the image.

rect1 = canvas.create_rectangle(238.0, 368.0, 268.0, 398.0, fill="#000000", outline="")
rect2 = canvas.create_rectangle(238.0, 418.0, 268.0, 448.0, fill="#000000", outline="")
rect3 = canvas.create_rectangle(238.0, 464.0, 268.0, 494.0, fill="#000000", outline="")
rect4 = canvas.create_rectangle(238.0, 512.0, 268.0, 542.0, fill="#000000", outline="")
rect5 = canvas.create_rectangle(238.0, 560.0, 268.0, 590.0, fill="#000000", outline="")

# Start the update loop
update_colors()

# Set the window title, icon and size
window.resizable(False, False)
myappid = 'tkinter.python.test'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
window.iconbitmap(relative_to_assets("icon.ico"))
window.title("Pycamo:Camo Generator")
window.mainloop()
