import cv2
import numpy as np
import matplotlib.pyplot as plt
from cellpose import models, io

#from file_retrieval import get_file_path

#Code with watershed, works badly...

img_path = "/Users/alenachen/Downloads/images/14.jpg"
img_bgr = cv2.imread(img_path)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)


#evening out contrast    
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
gray_eq = clahe.apply(gray)

#denoising + blur
denoise = cv2.fastNlMeansDenoising(gray_eq, None, 10, 7, 15)
blur = cv2.medianBlur(denoise, 7)

#edge detection
edges = cv2.Canny(blur, 5, 45)

#making b&w background and foreground
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#cleaning
kernel = np.ones((3,3), np.uint8)
mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

#separation of cells
dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
dist_norm = cv2.normalize(dist, None, 0, 1.0, cv2.NORM_MINMAX)

#threshold again with new info
_, sure_fg = cv2.threshold(mask, 0.6*mask.max(), 255, cv2.THRESH_BINARY)
sure_fg = np.uint8(sure_fg)

sure_bg = cv2.dilate(mask, kernel, iterations=3)
unknown = cv2.subtract(sure_bg, sure_fg)

#markers for watershed
_, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0

# watershed
img_color = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
markers = cv2.watershed(img_color, markers)

#Mark boundaries in green
img_color[markers == -1] = [0, 255, 0]

#counting
unique_labels = np.unique(markers)
cell_count = len(unique_labels[(unique_labels != -1) & (unique_labels != 0)])

print("Number of cells found:", cell_count)

plt.subplot(1,2,1); plt.imshow(thresh,cmap='gray')
plt.subplot(1,2,2); plt.imshow(img_color)
plt.show()