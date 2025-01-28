import os
from pathlib import Path
import ctypes
import numpy as np
from PIL import Image, ImageTk
import warnings
warnings.filterwarnings('ignore')
from skimage.filters.rank import modal
from tkinter import messagebox
#from tkinter import *
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, IntVar, Checkbutton, filedialog

class AssetsHelper:
    def __init__(self, assets_folder: str):
        self.assets_path = Path(__file__).parent.resolve() / assets_folder

    def get_asset_path(self, filename: str) -> Path:
        return self.assets_path / filename

class TkinterUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720")
        self.root.configure(bg="#1E2124")
        
        self.canvas = Canvas(
            self.root,
            bg="#1E2124",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)


        # Initialize assets helper
        self.assets_helper = AssetsHelper("assets/frame0")

        # UI Elements
        self._create_ui()

        # Update colors preview
        self.update_colors()

        # Setup window
        self.setup_window()

    def setup_window(self):
        # Set app ID for Windows taskbar
        myappid = 'pycamo.camogenerator.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        # Get the directory containing the script
        script_dir = Path(__file__).parent.resolve()
        icon_path = script_dir / "assets" /"frame0" / "icon.ico"
        # Set window properties
        self.root.iconbitmap(icon_path)
        self.root.title("Pycamo: Camo Generator")
        self.root.resizable(False, False)

    def update_colors(self):
            fills = []
            for self.entry in [self.entry_Cl1, self.entry_Cl2, self.entry_Cl3, self.entry_Cl4, self.entry_Cl5]:
                color = self.entry.get()
                if len(color) == 6 and all(c in '0123456789ABCDEFabcdef' for c in color):
                    fills.append("#" + color)
                else:
                    fills.append("#000000")
            
            self.canvas.itemconfig(self.rect1, fill=fills[0])
            self.canvas.itemconfig(self.rect2, fill=fills[1])
            self.canvas.itemconfig(self.rect3, fill=fills[2])
            self.canvas.itemconfig(self.rect4, fill=fills[3])
            self.canvas.itemconfig(self.rect5, fill=fills[4])
            
            self.root.after(100, self.update_colors)

        

    def _create_ui(self):
        # Preview text
        self.canvas.create_text(
            730.0, 28.0, anchor="nw", text="Preview ( Preview window size is 500x500 )",
            fill="#FFFFFF", font=("Inter", 24 * -1)
        )

        # Parameter text
        self.canvas.create_text(
            96.0, 28.0, anchor="nw", text="Parameter",
            fill="#FFFFFF", font=("Inter", 24 * -1)
        )

        # Parameter canvas
        self.canvas.create_rectangle(15.0, 86.0, 662.0, 649.0, fill="#444B53", outline="")

        # Preview canvas
        self.canvas.create_rectangle(706.0, 97.0, 1206.0, 597.0, fill="#D9D9D9", outline="")

        # Buttons
        self._create_buttons()

        # Entry boxes
        self._create_entries()

        # Parameter names
        self.canvas.create_text(52.0, 342.0, anchor="nw", text="Color", fill="#FFFFFF", font=("Inter", 24 * -1))
        self.canvas.create_text(322.0, 341.0, anchor="nw", text="Percent", fill="#FFFFFF", font=("Inter", 24 * -1))
        self.canvas.create_text(280.0, 173.0, anchor="nw", text="Color extract", fill="#FFFFFF", font=("Inter", 24 * -1))
        self.canvas.create_text(470.0, 342.0, anchor="nw", text="C value", fill="#FFFFFF", font=("Inter", 24 * -1))
        self.canvas.create_text(
            466.0, 409.0, anchor="nw",
            text="""    C value will 
    affect the result. 
    Look github repo 
    for more information""",
            fill="#FFFFFF", font=("Inter", 16 * -1)
        )


        # Pixel style checkbox
        self.pixel_style = IntVar()
        self.pixel_style.set(0)
        self.check_pixel = Checkbutton(
            self.root, text="Pixel style", variable=self.pixel_style, onvalue=1, offvalue=0
        )
        self.check_pixel.place(x=550.0, y=180.0)

    def _create_buttons(self):
        button_image_1 = PhotoImage(file=self.assets_helper.get_asset_path("button_1.png"))
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.load_image,
            relief="flat",
            bg="#1E2124",
            activebackground="#1E2124"
        )
        button_1.image = button_image_1  # Keep a reference to avoid garbage collection
        button_1.place(x=316.0, y=91.0, width=212.0, height=67.0)

        # Save camo button
        button_image_2 = PhotoImage(file=self.assets_helper.get_asset_path("button_2.png"))
        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_generated_camo,
            relief="flat",
            bg="#1E2124",
            activebackground="#1E2124"
        )
        button_2.image = button_image_2
        button_2.place(x=437.0, y=287.0, width=182.0, height=42.0)

        # Generate camo button
        button_image_3 = PhotoImage(file=self.assets_helper.get_asset_path("button_3.png"))
        button_3 = Button(
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.generate_pattern_from_entries,
            relief="flat",
            bg="#1E2124",
            activebackground="#1E2124"
        )
        button_3.image = button_image_3
        button_3.place(x=246.0, y=287.0, width=183.0, height=42.0)

    def _create_entries(self):
        # C value entry
        self.entry_Cvalue = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_Cvalue.place(x=466.0, y=372.0, width=174.0, height=28.0)
        # Extract color entry
        self.entry_Numcolor = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_Numcolor.place(x=249.0, y=173.0, width=24.0, height=28.0)

        #  colors entry

        # Group Cl: Color entries
        self.entry_Cl1 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_Cl1.place(x=50.0, y=369.0, width=174.0, height=28.0)

        
        self.entry_Cl2 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_Cl2.place(x=50.0, y=417.0, width=174.0, height=28.0)

        
        self.entry_Cl3 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_Cl3.place(x=50.0, y=465.0, width=174.0, height=28.0)

        
        self.entry_Cl4 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_Cl4.place(x=50.0, y=513.0, width=174.0, height=28.0)


        self.entry_Cl5 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_Cl5.place(x=50.0, y=561.0, width=174.0, height=28.0)

        # Group P: Percent entries
        
        self.entry_p1 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_p1.place(x=338.0, y=368.0, width=70.0, height=28.0)

        
        self.entry_p2 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_p2.place(x=338.0, y=416.0, width=70.0, height=28.0)

        
        self.entry_p3 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_p3.place(x=338.0, y=464.0, width=70.0, height=28.0)

        
        self.entry_p4 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_p4.place(x=338.0, y=512.0, width=70.0, height=28.0)

        
        self.entry_p5 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_p5.place(x=338.0, y=560.0, width=72.0, height=28.0)
        # create 2 entry boxes for camo size 
        self.entry_size1 = Entry( bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_size2 = Entry( bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_size1.place( x=380.0, y=220.0, width=54.0, height=28.0)
        self.entry_size2.place( x=300.0, y=220.0, width=54.0, height=28.0)        
        self.canvas.create_text( 360.0, 220.0, anchor="nw", text="x", fill="#FFFFFF", font=("Inter", 24 * -1))
        self.canvas.create_text( 250.0, 220.0, anchor="nw", text="size", fill="#FFFFFF", font=("Inter", 24 * -1))


        # Pixel size entry
        self.entry_pixel_size = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_pixel_size.place(x=560.0, y=220.0, width=74.0, height=28.0)
        self.canvas.create_text(450.0, 220.0, anchor="nw", text="Pixel size", fill="#FFFFFF", font=("Inter", 24 * -1))

        # Group Rect: Rectangles 
        self.rect1 = self.canvas.create_rectangle(238.0, 368.0, 268.0, 398.0, fill="#000000", outline="")
        self.rect2 = self.canvas.create_rectangle(238.0, 418.0, 268.0, 448.0, fill="#000000", outline="")
        self.rect3 = self.canvas.create_rectangle(238.0, 464.0, 268.0, 494.0, fill="#000000", outline="")
        self.rect4 = self.canvas.create_rectangle(238.0, 512.0, 268.0, 542.0, fill="#000000", outline="")
        self.rect5 = self.canvas.create_rectangle(238.0, 560.0, 268.0, 590.0, fill="#000000", outline="")


    loaded_image = None
    current_generated_image = None
    def load_image(self):
        global loaded_image
        # Open file explorer window to select the image
        from tkinter import filedialog
        file_path = filedialog.askopenfilename()
        # display the image in the Input image canvas
        img = Image.open(file_path)
        img = img.resize((200, 200), Image.LANCZOS)
        loaded_image = ImageTk.PhotoImage(img)
        self.image_container = self.canvas.create_image(
            138.0, 229.0, 
            image=loaded_image,
            tags="image"
        )
        
        # Raise image to top
        self.canvas.tag_raise(self.image_container)
        #self.canvas.create_image(138.0, 229.0, image=loaded_image)
        #self.canvas.image = loaded_image
        # Extract color palette, use number of colors extracted as the number of colors in entry_Numcolor if it is empty use 5 as default.
        if self.entry_Numcolor.get() == "":
            num_colors = 5
        else:
            num_colors = int(self.entry_Numcolor.get())
        colors_hex = self.extract_palette(file_path, num_colors)
        # fill the extracted colors in the color entry boxes.
        for i, color in enumerate(colors_hex):
            entry = eval(f"self.entry_Cl{i+1}")
            entry.delete(0, "end")
            entry.insert(0, color)
    # Extract colors from the image
    def median_cut(self,pixels, num_colors):
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

    def get_palette(self,boxes):
        return [tuple(map(int, np.mean(box, axis=0))) for box in boxes]

    def convert_palette_to_hex(self,palette):
        return [f"{r:02x}{g:02x}{b:02x}" for r, g, b in palette]

    def extract_palette(self,image_path, num_colors=5):
        image = Image.open(image_path).convert("RGB")
        image = image.resize((500, 500))
        # Convert to pixels
        pixels = np.array(list(image.getdata()))
        # Process
        boxes = self.median_cut(pixels, num_colors)
        palette = self.get_palette(boxes)
        hex_colors = self.convert_palette_to_hex(palette)
        print(hex_colors)
        return hex_colors
###################### Camogen ######################
# Convert hex color to RGB
    def hex2rgb(self,hex: str):
        return [int(hex[i:i+2], 16) for i in (0, 2, 4)]
    
    # Generate filtered noise image
    def nat_filt_im(self,size=(), c=2.0):
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
    ###### Generate camo pattern ######  new algorithm to generate camo pattern now :))
    def generate_pattern(self,colors_hex, output_filename, size=(), c=2.0, ratios=None):
        fp = np.ones((3, 3)).astype(np.uint8)
        
        # Filter out colors with zero ratios 
        if ratios is not None:
            non_zero_indices = [i for i, r in enumerate(ratios) if r > 0]
            colors_hex = [colors_hex[i] for i in non_zero_indices]
            ratios = [ratios[i] for i in non_zero_indices]
        
        rgb_colors = [self.hex2rgb(c.strip()) for c in colors_hex]
        palette = []
        for cc, hex in zip(rgb_colors, colors_hex):
            palette += cc

        n_colors = len(colors_hex)
        
        if ratios is None:
            ratios = [1 / n_colors] * n_colors
        else:
            assert len(ratios) == n_colors, messagebox.showerror("Error", "Please fill color percentages")
            assert np.isclose(sum(ratios), 100), messagebox.showerror("Error", "Sum of color percentages should be 100") 
            ratios = np.array(ratios) / sum(ratios)

        # Generate separate noise layers only for non-zero colors
        noise_layers = [self.nat_filt_im(size=size, c=c) for _ in range(n_colors)]
        
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
        if output_filename:  # Only save if filename is provided
            img.save(output_filename)
        return img
    ##### pixel camo style ####
    def pixelize_image(self,current_generated_image, pixel_size=10):
        # Load the image
        image = current_generated_image
        # Resize the image to a smaller size
        small_image = image.resize(
            (image.width // pixel_size, image.height // pixel_size), Image.NEAREST)
        # Resize back to the original size
        pixelated_image = small_image.resize(image.size, Image.NEAREST)
        return pixelated_image
    def save_generated_camo(self):
        print("Save generated camo functionality not implemented yet.")

    def generate_pattern_from_entries(self):
        global current_generated_image  # Add this to track current generated image
    
        # Collect colors from entry boxes, ignoring blank entries
        colors_hex = [self.entry_Cl1.get(), self.entry_Cl2.get(), self.entry_Cl3.get(), self.entry_Cl4.get(), self.entry_Cl5.get()]
        colors_hex = [color for color in colors_hex if color]  # Filter out empty color entries
        
        # Collect ratios from entry boxes
        ratios = [self.entry_p1.get(), self.entry_p2.get(), self.entry_p3.get(), self.entry_p4.get(), self.entry_p5.get()]
        ratios = [float(r) for r in ratios if r]  # Filter out empty ratio entries
        if "" in ratios:
            ratios = None
        else:
            ratios = [float(r) for r in ratios]
        
        # Default value for entry_Cvalue if empty
        if self.entry_Cvalue.get() == "":
            self.entry_Cvalue.insert(0, "1.2")
        # check if the camo size entry boxes are empty if empty show error message.
        if self.entry_size1.get() == "" or self.entry_size2.get() == "":
            messagebox.showerror("Error", "Please fill camo size")
        
        # Check if the check box is checked if checked pixelize the image and save it to the output folder.
        if self.pixel_style.get() == 1:
            img = self.generate_pattern(colors_hex, None, (int(self.entry_size1.get()), int(self.entry_size2.get())), 
                            c=float(self.entry_Cvalue.get()), ratios=ratios)
            if self.entry_pixel_size.get() == "":
                messagebox.showerror("Error", "Please fill pixel size")
            else: 
                img = self.pixelize_image(img, pixel_size=int(self.entry_pixel_size.get()))  
        else:
            # Generate the pattern without saving
            img = self.generate_pattern(colors_hex, None, (int(self.entry_size1.get()), int(self.entry_size2.get())), 
                            c=float(self.entry_Cvalue.get()), ratios=ratios)
        

        current_generated_image = img  # Store the generated image
        
        # Display the generated pattern in the preview canvas
        display_img = img.resize((500, 500), Image.LANCZOS)
        photo_img = ImageTk.PhotoImage(display_img)
        self.canvas.create_image(956.0, 347.0, image=photo_img)
        self.canvas.image = photo_img

if __name__ == "__main__":
    root = Tk()
    app = TkinterUI(root)
    root.mainloop()
