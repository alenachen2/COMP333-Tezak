from PIL import Image 
from tkinter import Tk, filedialog

image_path = "path_name"

# Hide the root window
Tk().withdraw()

# Ask the user to select an image file
file_path = filedialog.askopenfilename(
    title="Select an image file",
    filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
)

if file_path:
    print("Selected image path:", file_path)
else:
    print("No file selected.")


try:
    img = Image.open(image_path)

    img.show()

except FileNotFoundError:
     print(f"Error: The file '{image_path}' was not found.")
except IOError:
    print(f"Error: Could not open or identify the image file '{image_path}'.")