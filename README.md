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

Now you can use Pycamo with a GUI!. Just run `GUI.py` and enjoy.

![Update Screenshot](https://github.com/user-attachments/assets/615ca98e-bfb3-4392-9003-cc69a1c48d05)

---

## How It Works?

This camouflage pattern generator is based on fractal noise. Below is an overview of its working process:

### 1. Extract Colors

The first step involves extracting the main colors from an input image.

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

## How to Use

Follow these steps to use the Camouflage Pattern Generator:

### 1. Clone the Project Repository
Download the project to your local machine using Git:

```bash
git clone https://github.com/your-repo-link.git
cd your-repo-folder
```

Install library

```
pip install -r requirements.txt
```

Then you can run Camogen 

```
python camogen.py
```

You can edit parameter here 

![image](https://github.com/user-attachments/assets/738b57d9-7767-48c4-982e-c81943b413f1)

| **Parameter**       | **Description**                                                                 |
|----------------------|---------------------------------------------------------------------------------|
| `color_palette`      | A list of colors extracted from an image or defined manually.                  |
| `num_colors`         | The number of colors to extract from the image using the `extract_palette` function. |
| `ratios`             | A list of percentages defining how much each color should contribute to the pattern. |
| `size`               | The dimensions of the generated camouflage pattern in pixels (width, height).  |
| `c`                  | A parameter that controls the complexity of the fractal noise.                 |
| `ratios=ratios`      | Passes the predefined ratios for each color to the `generate_pattern` function. |
| `"demo_input/teste3.png"` | The input image file used to extract colors.                                 |
| `"gencamo.png"`      | The output file name where the generated pattern will be saved.                 |



To use GUI instead of command. 

```
cd to GUI folder
```

then 

```
python GUI.py
```

ENJOY!

![Update Screenshot](https://github.com/user-attachments/assets/615ca98e-bfb3-4392-9003-cc69a1c48d05)






