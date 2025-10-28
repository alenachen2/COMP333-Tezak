from PIL import Image 

#user manually opens this file and pastes file name
image_path : str 

try:
    image_path = input("paste your file path here: ")

except FileNotFoundError:
     print(f"Error: The file '{image_path}' was not found. Run the program again.")
except IOError:
    print(f"Error: Could not open or identify the image file '{image_path}'.")

img = Image.open(image_path)

img.show()