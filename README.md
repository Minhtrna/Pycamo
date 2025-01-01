# Update

Now you can create camouflage with each color having it's own ratio. The automatically generated camouflage result may not guarantee an even color distribution in every run. When no color ratio was given, the algorithm would randomly inject colors into the image. But now we can give specific ratios for each color like: ratio = [25, 25, 25, 25] (equal ratio for all colors) or ratio = [20, 25, 35, 20] and it will ensure that the result will always have an even color distribution.

![update](https://github.com/user-attachments/assets/d1e1374e-10d7-4de1-855a-18ac6f02e18b)


# Camouflage Pattern Generator 

![Camouflage Pattern Generator](https://github.com/user-attachments/assets/fc3c84c4-ce5c-4c6e-8883-b49da995d693)

## How it's work?

#### This camouflage pattern generator base on fractal noise.

### 1. Extract color from image.

![image](https://github.com/user-attachments/assets/5c20d5a4-dee0-44fa-b9ec-ee092a0c42e1)

### you can edit the number of color you want to extract by edit the "num_colors" 
#### ex: color_palette = cp.extract_palette("demo_input/k20r.jpg", num_colors=4) # extract 4 main color from the image.

### 2. Generate fractal noise and fill color

#### Fractals are generated randomly within a specified given frame size . 

#### ex : generate_pattern(color_palette, "gencamo.png", size=(500, 500), c= 3).

#### The C value will affect the final result. Look the image for better understand.

![image](https://github.com/user-attachments/assets/5b6bfb01-764f-4b06-965c-9e2ee07607f6)


## How to use?
#### Clone project and then run the camogen.py file 

![image](https://github.com/user-attachments/assets/5a74f793-41f9-427e-99cb-72dc2f00ef71)





