import cv2
import numpy as np
import matplotlib.pyplot as plt

from file_retrieval import get_file_path

class cell:
    def __init__(self):
        self.data = []

#User test function 
def classify_cell(cell): 
    if cell["color"] == "red": 
        return "Cell Identified"
    else: 
        return "Not a Cell"

def count_cells(cell_list): 
    count_cell = 0 
    count_notcell = 0
    for cell in cell_list: 
        if classify_cell(cell) == "Cell Identified": 
            count_cell += 1
        else: 
            count_notcell += 1
    return{"Cells Identified": count_cell, "Cells Not Identified": count_notcell}


#loading image, make it work together with accessing_files.py
#img = cv2.imread('insert path here')
img_path = file_retrieval()
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#blurring to reduce noise
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
gray_eq = clahe.apply(gray)
blur = cv2.GaussianBlur(gray_eq, (5,5), 0)

thresh = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 41, 2
)

kernel = np.ones((3,3), np.uint8)
clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
clean = cv2.dilate(clean, kernel, iterations=1)

#distance transform — helps split touching cells
dist = cv2.distanceTransform(clean, cv2.DIST_L2, 5)
dist_norm = cv2.normalize(dist, None, 0, 1.0, cv2.NORM_MINMAX)

_, sure_fg = cv2.threshold(dist_norm, 0.4, 1.0, cv2.THRESH_BINARY)
sure_fg = np.uint8(sure_fg * 255)

#identify background and unknown regions
sure_bg = cv2.dilate(clean, kernel, iterations=3)
unknown = cv2.subtract(sure_bg, sure_fg)

_, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0

# watershed
img_color = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
markers = cv2.watershed(img_color, markers)

# Mark boundaries in green
#img_color[markers == -1] = [0, 255, 0]

# display graphs
plt.figure(figsize=(15,5))
plt.subplot(1,2,1); plt.imshow(gray, cmap='gray'); plt.title('Enhanced Grayscale')
plt.subplot(1,2,2); plt.imshow(clean, cmap='gray'); plt.title('Binary Mask')
#plt.subplot(1,3,3); plt.imshow(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)); plt.title('Boundaries Marked')
plt.show()
