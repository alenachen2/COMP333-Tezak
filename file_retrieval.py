from PIL import Image 

def get_file_path():
    """prompts user to copy the desired image's filepath and returns it"""
    image_path : str 

    try:
        image_path = input("paste your file path here: ")

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found. Try again.")
        get_file_path()
    except IOError:
        print(f"Error: Could not open or identify the image file '{image_path}'.")

    return image_path

#img = Image.open(image_path)
