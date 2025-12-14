from file_retrieval import get_file_path
import cv2
import numpy as np

def multiple_images():
    '''
    Allows user put in multiple file paths instead of just one. Store the file paths in a list.
    Input: None
    Output: array of images from the inputed file paths.
    '''
    imgs_array = []
    all_paths = []
    while True:
        img_path = get_file_path()
        if img_path in all_paths:
            add = input("This image has already been added. Do you want to add it again? Y or N\n").strip().upper()
            if add == 'Y':
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                imgs_array.append(img)
            else: 
                print ("Image was not added.")
        else:
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgs_array.append(img)
            all_paths.append(img_path)
        again = input("Would you like to add another file? Y or N\n").strip().upper()
        if again == 'N':
            break
    return imgs_array