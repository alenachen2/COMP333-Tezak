import cv2
from yaspin import yaspin
from yaspin.spinners import Spinners
from file_retrieval import get_file_path
from cell_identification import split_channels
from cell_identification import clean
from cell_identification import create_model
from cell_identification import classify_cells_by_color
from cell_identification import display_results
from cell_counting import count
from multiple_files import multiple_images
import numpy as np

if __name__ == "__main__":
    
    img_array = multiple_images()

    print("Processing image...")

    for img in img_array:

        with yaspin(text="Identifying cells...", color="yellow") as spinner:
        
            model = create_model()

            masks, flows, styles = model.eval(
                img,
                flow_threshold=0.4,
                cellprob_threshold=0.0,
                normalize = True, 
                diameter = None
            )

            all_counts = classify_cells_by_color(img, masks)
        
        print("Cell segmentation complete. Extracting color ROIs...")
        print("Total cells detected: " + str(count(np.unique(masks))))
        print("Red cells detected: " + str(all_counts["red"]))
        print("Green cells detected: " + str(all_counts["green"]))
        print("Blue cells detected: " + str(all_counts["blue"]))
        display_results(img, masks, flows)