# Update

Now you can use Pycamo with GUI. Cannot build it to exe file, windows say it's a virus :)) i'm not 100% trust any packaging tools so... Let's run GUI.py and enjoy.

![image](https://github.com/user-attachments/assets/615ca98e-bfb3-4392-9003-cc69a1c48d05)



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





