# Camouflage Pattern Generator

![Camouflage Pattern Generator](https://github.com/user-attachments/assets/fc3c84c4-ce5c-4c6e-8883-b49da995d693)

---

## Table of Contents
1. [Update](#update)  
2. [How It Works?](#how-it-works)  
   - [Extract Colors](#extract-colors)  
   - [Generate Fractal Noise and fill with colors](#generate-fractal-noise)  
3. [How to Use](#how-to-use)

---

## Update

Pycamo can generate pixel camo now! Check the box if u want, also i rewrite file save function and Camo generate algorithm too it better now. ENJOY!!

![image](https://github.com/user-attachments/assets/94d331a7-c8c4-4b1f-b329-8fa41f07f0c0)



---

## How It Works?

This camouflage pattern generator is based on fractal noise.

### 1. Extract Colors

The first step is extract main colors from an input image.

![Extract Colors](https://github.com/user-attachments/assets/5c20d5a4-dee0-44fa-b9ec-ee092a0c42e1)

You can customize the number of colors to extract by modifying the `num_colors` parameter. For example:

```python
color_palette = cp.extract_palette("demo_input/k20r.jpg", num_colors=4)  # Extract 4 main colors
```

### 2. Generate Fractal Noise

In this step, fractals are randomly generated within a given frame size and filled with the extracted colors. You can control the parameters to customize the final camouflage pattern.

#### Example:
```python
generate_pattern(color_palette, "gencamo.png", size=(500, 500), c=3)
```

![image](https://github.com/user-attachments/assets/145a31ce-73c7-49dc-9cf3-edf13d90b646)

Pycamo can generate 2 type of digital camo: Fractal and pixel.

![Camouflage Pattern Generator](https://github.com/user-attachments/assets/5b31e80c-5f0b-4117-91ff-eef7f15abc37)


## How to Use

Follow these steps to use the Camouflage Pattern Generator:

### 1. Clone the Project Repository

```
git clone https://github.com/Minhtrna/Pycamo.git
```

Install library

```
pip install -r requirements.txt
```

Then you can run Pycamo in ```scr``` folder

```
python Pycamo.py
```

Or

Use Pycamo in other Py program by

```
import Pycamo
```


You can edit parameter here 

![image](https://github.com/user-attachments/assets/8af52403-a055-4f43-a4ff-841c4c56eb56)



| **Parameter**       | **Description**                                                                 |
|----------------------|---------------------------------------------------------------------------------|
| `color_palette`      | A list of colors extracted from an image or defined manually.                  |
| `num_colors`         | The number of colors to extract from the image using the `extract_palette` function. |
| `ratios`             | A list of percentages defining how much each color should contribute to the pattern. |
| `size`               | The dimensions of the generated camouflage pattern in pixels (width, height).  |
| `c`                  | A parameter that controls the complexity of the fractal noise.                 |
| `ratios=[]`      | Passes the predefined ratios for each color to the `generate_pattern` function. |
| `pixelize=True/False`  | Set True to pixelize camo, False for normal fractal. |
| `pixel_size`  | Set pixel size for pixelize function. |
| `"demo_input/teste3.png"` | The input image file used to extract colors.                                 |
| `"gencamo.png"`      | The output file name where the generated pattern will be saved.                 |



To use GUI instead of command. 

```
go to GUI folder
```

then 

```
python GUI.py
```

ENJOY!

![image](https://github.com/user-attachments/assets/94d331a7-c8c4-4b1f-b329-8fa41f07f0c0)






