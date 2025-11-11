import cv2
import numpy as np
import matplotlib.pyplot as plt

#from file_retrieval import get_file_path
"""
class cell:
    def __init__(self):
        self.data = []


#User test function 
def classify_cell(cell): 
    ''' 
    Determines if input is a cell or not.

    Args: 
        cell: an object in the cell class

    Returns: 
        bool: True if arg cell is a cell, false if arg cell is not a cell
    '''
    if cell["color"] == "red": 
        return "Cell Identified"
    else: 
        return "Not a Cell"


def count_cells(cell_list): 
    ''''
    Counts the number of cells in a given list.

    Args:
        cell_list: A list of cell types

    Returns:
        int: number of successfully counted cells
        int: number of unsuccessfully counted cells
    '''
    count_cell = 0 
    count_notcell = 0
    for cell in cell_list: 
        if classify_cell(cell) == "Cell Identified": 
            count_cell += 1
        else: 
            count_notcell += 1
    return{"Cells Identified": count_cell, "Cells Not Identified": count_notcell}
"""



#Code with watershed, works badly...

img_path = "/Users/allegracuriel/Downloads/images/2.jpg"
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


#this commented out section also works but badly (I think)

"""

img_path = "/Users/allegracuriel/Downloads/images/23.jpg"
img_bgr = cv2.imread(img_path)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

#increasing contrast    
clahe = cv2.createCLAHE(clipLimit=0.5)
gray_eq = clahe.apply(gray)

#denoise
denoise = cv2.fastNlMeansDenoising(gray_eq, None, 10, 7, 15)
#blur1 = cv2.GaussianBlur(denoise, (5,5), 0)
#blur1 = cv2.medianBlur(denoise, 15)
blur = cv2.medianBlur(denoise, 21)
edges = cv2.Canny(blur, 5, 45)

thresh = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV, 31, 2
)


kernel = np.ones((5,5), np.uint8)
#mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
#mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print("Number of Contours Found = " + str(len(contours)))
cv2.drawContours(img_bgr, contours, -1, (0, 255, 0), 3)

plt.subplot(1,4,1); plt.imshow(gray, cmap = 'gray')
plt.subplot(1,4,2); plt.imshow(gray_eq, cmap='gray')
plt.subplot(1,4,3); plt.imshow(thresh,cmap='gray')
plt.subplot(1,4,4); plt.imshow(img_bgr)
plt.show()
"""


#Old watershedding stuff
"""
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
"""
