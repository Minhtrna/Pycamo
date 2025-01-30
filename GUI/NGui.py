# This file contains the UI and UI logic for the Camo Generator
from pathlib import Path
import ctypes
from PIL import Image, ImageTk
import warnings
warnings.filterwarnings('ignore')
from skimage.filters.rank import modal
from tkinter import messagebox
#from tkinter import *
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, IntVar, Checkbutton, filedialog
import Camologic


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
        self.ui_functions = Uifunctions(self)
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

        # Input image text
        self.canvas.create_text(
            72.0, 90.0, anchor="nw", text="Input Image",
            fill="#FFFFFF", font=("Inter", 24 * -1)
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
            command=self.ui_functions.load_image,
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
            command=self.ui_functions.save_generated_camo,
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
            command=self.ui_functions.generate_pattern_from_entries,
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

class Uifunctions:
    def __init__(self, ui_instance):
        
        # Store TkinterUI instance directly
        self.ui = ui_instance
        # Get canvas reference from UI instance
        self.canvas = self.ui.canvas
        self.current_generated_image = None
        

    def load_image(self):
        global loaded_image
        # Open file explorer window to select the image
        from tkinter import filedialog
        file_path = filedialog.askopenfilename()
        # display the image in the Input image canvas
        img = Image.open(file_path)
        img = img.resize((200, 200), Image.LANCZOS)
        loaded_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(138.0, 229.0, image=loaded_image)
        self.canvas.image = loaded_image
        # Extract color palette, use number of colors extracted as the number of colors in entry_Numcolor if it is empty use 5 as default.
        if self.ui.entry_Numcolor.get() == "":
            num_colors = 5
        else:
            num_colors = int(self.ui.entry_Numcolor.get())
        colors_hex = Camologic.extract_palette(file_path, num_colors)
        # fill the extracted colors in the color entry boxes.
        # clear the entry boxes first to avoid appending to the existing colors.
        for entry in [self.ui.entry_Cl1, self.ui.entry_Cl2, self.ui.entry_Cl3, self.ui.entry_Cl4, self.ui.entry_Cl5]:
            entry.delete(0, "end")
        for i, color in enumerate(colors_hex):
            self.canvas.itemconfig(f"rect{i+1}", fill=color)
            entry = [self.ui.entry_Cl1, self.ui.entry_Cl2, self.ui.entry_Cl3, self.ui.entry_Cl4, self.ui.entry_Cl5][i]
            entry.insert(0, color)
            

    def generate_pattern_from_entries(self):
        global current_generated_image
        
        colors_hex = []
        # Collect colors from entry boxes, ignoring blank entries
        colors_hex = [self.ui.entry_Cl1.get(), self.ui.entry_Cl2.get(), self.ui.entry_Cl3.get(), self.ui.entry_Cl4.get(), self.ui.entry_Cl5.get()]
        colors_hex = [color for color in colors_hex if color]

        # Check if we have any colors before proceeding
        if not colors_hex:
            messagebox.showerror("Error", "Please enter at least one color")
            return

        # Collect ratios from entry boxes
        ratio_entries = [self.ui.entry_p1, self.ui.entry_p2, self.ui.entry_p3, self.ui.entry_p4, self.ui.entry_p5]
        ratios = []
        for i in range(len(colors_hex)):
            ratio_str = ratio_entries[i].get()
            if ratio_str:
                ratios.append(float(ratio_str))
            else:
                ratios.append(0.0)
        # Auto-fill empty ratios if needed
        if sum(ratios) != 100:
            # Clear the entry boxes first to avoid appending to the existing ratios
            for entry in ratio_entries:
                entry.delete(0, "end")

            # Auto-fill ratios
            equal_ratio = round(100.0 / len(colors_hex), 4)
            ratios = []
            for i in range(len(colors_hex)):
                ratio_entries[i].insert(0, str(equal_ratio))
                ratios.append(equal_ratio)
            messagebox.showinfo("Info", "Ratios auto-filled to balance 100%")
                
            
        # Default value for entry_Cvalue if empty
        if self.ui.entry_Cvalue.get() == "":
            self.ui.entry_Cvalue.insert(0, "1.2")
        # check if the camo size entry boxes are empty if empty show error message.
        if self.ui.entry_size1.get() == "" or self.ui.entry_size2.get() == "":
            messagebox.showerror("Error", "Please fill camo size")
        
        # Check if the check box is checked if checked pixelize the image and save it to the output folder.
        if self.ui.pixel_style.get() == 1:
            img = Camologic.generate_pattern(colors_hex, None, (int(self.ui.entry_size1.get()), int(self.ui.entry_size2.get())), 
                            c=float(self.ui.entry_Cvalue.get()), ratios=ratios)
            if self.ui.entry_pixel_size.get() == "":
                messagebox.showerror("Error", "Please fill pixel size")
            else: 
                img = Camologic.pixelize_image(img, pixel_size=int(self.ui.entry_pixel_size.get()))  
        else:
            # Generate the pattern without saving
            img = Camologic.generate_pattern(colors_hex, None, (int(self.ui.entry_size1.get()), int(self.ui.entry_size2.get())), 
                            c=float(self.ui.entry_Cvalue.get()), ratios=ratios)
        

        current_generated_image = img  # Store the generated image
        
        # Display the generated pattern in the preview canvas
        display_img = img.resize((500, 500), Image.LANCZOS)
        photo_img = ImageTk.PhotoImage(display_img)
        self.canvas.create_image(956.0, 347.0, image=photo_img)
        self.canvas.image = photo_img
    
    def save_generated_camo(self):
        if current_generated_image:
        # Open file dialog for save location
            filetypes = [('PNG files', '*.png')]
            save_dir = Path(__file__).parent.resolve()
            output_file = filedialog.asksaveasfilename(
                defaultextension='.png',
                filetypes=filetypes,
                initialdir=save_dir,
                title="Save Camo Pattern"
            )
            
            if output_file:  # Check if user didn't cancel
                try:
                    current_generated_image.save(output_file)
                    messagebox.showinfo("Success", f"Camo pattern saved successfully to:\n{output_file}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = TkinterUI(root)
    root.mainloop()
