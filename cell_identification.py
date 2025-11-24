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

# --- split channels ---
b, g, r = cv2.split(img)

# --- RED CLEANING ---
# suppress blue/green bleed
red_clean = r.astype(np.int16) - (0.3 * b.astype(np.int16)) - (0.1 * g.astype(np.int16))
red_clean = np.clip(red_clean, 0, 255).astype(np.uint8)

# normalize contrast
red_clean = cv2.normalize(red_clean, None, 0, 255, cv2.NORM_MINMAX)

# --- BLUE CLEANING ---
# suppress red/green bleed
blue_clean = b.astype(np.int16) - (0.2 * r.astype(np.int16)) - (0.1 * g.astype(np.int16))
blue_clean = np.clip(blue_clean, 0, 255).astype(np.uint8)

# normalize contrast
blue_clean = cv2.normalize(blue_clean, None, 0, 255, cv2.NORM_MINMAX)

# --- GREEN CLEANING ---
# suppress red/blue bleed
green_clean = g.astype(np.int16) - (0.2 * r.astype(np.int16)) - (0.1 * b.astype(np.int16))
green_clean = np.clip(green_clean, 0, 255).astype(np.uint8) 

#Put into list for cellpose
imgs_clean_split = [red_clean, green_clean, blue_clean]

with yaspin(text="Identifying cells...", color="yellow") as spinner:
    #Create Cellpose model
    model = models.CellposeModel(pretrained_model='cpsam',gpu=True)

    #Segment image
    masks, flows, styles = model.eval(
        imgs_clean_split,
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
plot.show_segmentation(fig0, red_clean, masks[0], flows[0][0])
plt.tight_layout()
plt.show()

#display results - - to be changed
fig1 = plt.figure(figsize=(12,5))
plot.show_segmentation(fig1, green_clean, masks[1], flows[1][0])
plt.tight_layout()
plt.show()

#display results - - to be changed
fig2 = plt.figure(figsize=(12,5))
plot.show_segmentation(fig2, blue_clean, masks[2], flows[2][0])
plt.tight_layout()
plt.show()