from PIL import Image 

def get_file_path():
    """prompts user to copy the desired image's filepath and returns it"""
    imagePath : str 

    try:
        imagePath = input("paste your file path here: ")

    except FileNotFoundError:
        print(f"Error: The file '{imagePath}' was not found. Try again.")
        get_file_path()
    except IOError:
        print(f"Error: Could not open or identify the image file '{imagePath}'.")

    return imagePath

#img = Image.open(image_path)
