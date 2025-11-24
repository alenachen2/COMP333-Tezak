import cv2
import numpy as np
import matplotlib.pyplot as plt
import cellpose
from cellpose import models
from cellpose import io
from cellpose import plot
from yaspin import yaspin
from yaspin.spinners import Spinners
from file_retrieval import get_file_path

#Retrieve image path
img_path = get_file_path()

#Read image
img_bgr = cv2.imread(img_path)
img = img_bgr.copy()

def split_channels(image):
    '''
    Separates the image into blue, green, and red channels.
    Input: an image
    Output: 
        b: image with only the blue channel
        g: image with only the green channel
        r: image with only the red channel
    '''
    b, g, r = cv2.split(image)
    return b, g, r

b, g, r = split_channels(img)

def clean(b, g, r):
    '''
    Cleans up an image with an individual channel by suppressing the colors from the remaining
    two channels. For instance, cleaning up a red channel involves suppressing the blue and green
    bleed that may be leftover in the image.
    Input: 
        b: image with only the blue channel
        g: image with only the green channel
        r: image with only the red channel
    Output: a list of the clean and normalized red, green, and blue channels
    '''
    red_clean = r.astype(np.int16) - (0.3 * b.astype(np.int16)) - (0.1 * g.astype(np.int16))
    red_clean = np.clip(red_clean, 0, 255).astype(np.uint8)
    
    blue_clean = b.astype(np.int16) - (0.2 * r.astype(np.int16)) - (0.1 * g.astype(np.int16))
    blue_clean = np.clip(blue_clean, 0, 255).astype(np.uint8)
    
    green_clean = g.astype(np.int16) - (0.2 * r.astype(np.int16)) - (0.1 * b.astype(np.int16))
    green_clean = np.clip(green_clean, 0, 255).astype(np.uint8) 

    return [normalize(red_clean), normalize(green_clean), normalize(blue_clean)]


def normalize(image):
    '''
    Normalizes the contrast in the image.
    Input:
        image: an image
    Output:
        normalized image 
    '''
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)

imgs_clean_array = clean(b, g, r)


with yaspin(text="Identifying cells...", color="yellow") as spinner:
    def create_model():
        '''
        Create a Cellpose model.
        Output:
            model: model using Cellpose's pretrained model, cpsam
        '''
        model = models.CellposeModel(pretrained_model='cpsam',gpu=True)
        return model

    #Segment image
    masks, flows, styles = model.eval(
        imgs_clean_array,
        channels=[0,0],
        flow_threshold=0.3,
        cellprob_threshold=2.5,
    )

#Display results

#Get unique labels in masks which correspond to different ROIs detected
red_ROIs = np.unique(masks[0])
green_ROIs = np.unique(masks[1])
blue_ROIs = np.unique(masks[2])

#print results and subtract 1 to not count background
print(f"Red cells detected: {len(red_ROIs) - 1}"   
    f"\nGreen cells detected: {len(green_ROIs) - 1}"   
    f"\nBlue of cells detected: {len(blue_ROIs) - 1}")   

#display results - - to be changed
fig0 = plt.figure(figsize=(12,5))
plot.show_segmentation(fig0, imgs_clean_array[0], masks[0], flows[0][0])
plt.tight_layout()
plt.show()

#display results - - to be changed
fig1 = plt.figure(figsize=(12,5))
plot.show_segmentation(fig1, imgs_clean_array[1], masks[1], flows[1][0])
plt.tight_layout()
plt.show()

#display results - - to be changed
fig2 = plt.figure(figsize=(12,5))
plot.show_segmentation(fig2, imgs_clean_array[2], masks[2], flows[2][0])
plt.tight_layout()
plt.show()