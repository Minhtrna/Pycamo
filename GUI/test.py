from PIL import Image

def pixelize_image(image_path, output_path, pixel_size=10):
    # Load the image
    image = Image.open(image_path).convert("RGB")
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    # Resize the image to a smaller size
    small_image = image.resize(
        (image.width // pixel_size, image.height // pixel_size), Image.NEAREST)
    # Resize back to the original size
    pixelated_image = small_image.resize(image.size, Image.NEAREST)

    # Save the output image
    pixelated_image.save(output_path)
    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    input_image_path = "D:\Github\Pycamo\gencamo.png"
    output_image_path = "camo_pixelated.png"
    pixelize_image(input_image_path, output_image_path)