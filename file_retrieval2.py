from PIL import Image 

image_path = "path_name"

try:
    img = Image.open(image_path)

    img.show()

except FileNotFoundError:
     print(f"Error: The file '{image_path}' was not found.")
except IOError:
    print(f"Error: Could not open or identify the image file '{image_path}'.")