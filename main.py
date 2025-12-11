import cv2
from yaspin import yaspin
from yaspin.spinners import Spinners
from file_retrieval import get_file_path
from cell_identification import split_channels
from cell_identification import clean
from cell_identification import create_model
from cell_identification import segment
from cell_identification import extract_ROI
from cell_identification import display_results
from cell_identification import classify_cells_by_color
from cell_counting import count
import numpy as np

if __name__ == "__main__":
    img_path = get_file_path()
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print("Processing image...")
    
    b, g, r = split_channels(img)

    with yaspin(text="Identifying cells...", color="yellow") as spinner:
        model = create_model()
        #masks, flows, styles = segment(model, imgs_clean_array)

    print("Cell segmentation complete. Extracting color ROIs...")
    masks, flows, styles = model.eval(
            img,
            flow_threshold=0.4,
            cellprob_threshold=0.0,
            normalize = True, 
            diameter = None
        )
    all_counts = classify_cells_by_color(img, masks)

    print("Total cells detected: " + str(count(np.unique(masks))))
    print("Red cells detected: " + str(all_counts["red"]))
    print("Green cells detected: " + str(all_counts["green"]))
    print("Blue cells detected: " + str(all_counts["blue"]))
   
