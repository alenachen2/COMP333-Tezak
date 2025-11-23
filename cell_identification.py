import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import cellpose
from cellpose import models
from cellpose import io
from cellpose.io import imread
from cellpose import plot
from file_retrieval import get_file_path

#Retrieve image path
img_path = get_file_path()

#Read image
img_bgr = cv2.imread(img_path)
img = img_bgr.copy()

# --- split channels ---
b, g, r = cv2.split(img)

"""
# --- RED CLEANING ---
# suppress blue/green bleed
red_clean = r.astype(np.int16) - (0.3 * b.astype(np.int16)) - (0.1 * g.astype(np.int16))
red_clean = np.clip(red_clean, 0, 255).astype(np.uint8)

# normalize contrast
red_clean = cv2.normalize(red_clean, None, 0, 255, cv2.NORM_MINMAX)
"""
# --- BLUE CLEANING ---
# suppress red/green bleed
blue_clean = b.astype(np.int16) - (0.2 * r.astype(np.int16)) - (0.1 * g.astype(np.int16))
blue_clean = np.clip(blue_clean, 0, 255).astype(np.uint8)

# normalize contrast
blue_clean = cv2.normalize(blue_clean, None, 0, 255, cv2.NORM_MINMAX)


"""
cell_color_num = input("What color are the cells you want to identify? Type the corresponding number below: "
                   "\n1. Red cells"
                   "\n2. Green cells"
                   "\n3. Blue cells"
                   "\nCell color: ")
if cell_color_num == '1':
    print("Red cells selected.")
    img[:, :, 0] = 0
    img[:, :, 1] = 0
elif cell_color_num == '2':
    print("Green cells selected.")
    img[:, :, 0] = 0
    img[:, :, 2] = 0
elif cell_color_num == '3':
    print("Blue cells selected.")
    #Blue channel is channel 2 in RGB
    img[:, :, 1] = 0
    img[:, :, 2] = 0    
else:
    print("Invalid input. Proceeding with original image.")
"""
#Convert BGR to RGB so it displays correctly
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


#Create Cellpose model
model = models.CellposeModel(pretrained_model='cpsam',gpu=True)

#Segment image
masks, flows, styles = model.eval(
    blue_clean,
    flow_threshold=0.4, 
    cellprob_threshold=2.0,
)

#Display results

#Get unique labels in masks which correspond to different ROIs detected
labels = np.unique(masks)

#print results and subtract 1 to not count background
print(f"Number of cells detected: {len(labels) - 1}")   

#display results - - to be changed
fig = plt.figure(figsize=(12,5))
plot.show_segmentation(fig, img, masks, flows[0])
plt.tight_layout()
plt.show()