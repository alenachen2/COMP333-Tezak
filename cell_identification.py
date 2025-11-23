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
#Convert BGR to RGB so it displays correctly
img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

#Create Cellpose model
model = models.CellposeModel(gpu=True)

#Segment image
masks, flows, styles = model.eval(
    img,
    flow_threshold=0.4, 
    cellprob_threshold=0.0,   # grayscale
)


#Display results

#Get unique labels in masks which correspond to different ROIs detected
labels = np.unique(masks)

#print results and subtract 1 to not count background
print(f"Number of cells detected: {len(labels) - 1}")   
fig = plt.figure(figsize=(12,5))
plot.show_segmentation(fig, img, masks, flows[0])
plt.tight_layout()
plt.show()