import cv2
import numpy as np

from cell_identification import (
    create_model,
    classify_cells_by_color,
    display_results,   # not used in GUI but kept for parity
)
from cell_counting import count


def run_pipeline(img):
    '''
    Run the same pipeline as main.py, but on an in-memory image
    instead of reading from a file.
    Input:
        img: numpy array, RGB image (same as in main.py after cvtColor)
    Output:
        masks: 2D array of Cellpose labels
        flows: Cellpose flows (for visualization if needed)
        all_counts: dict with keys 'red', 'green', 'blue'
        total_cells: int, total number of cells detected
    '''

    model = create_model()

    masks, flows, styles = model.eval(
        img,
        flow_threshold=0.4,
        cellprob_threshold=0.0,
        normalize=True,
        diameter=None,
    )

    all_counts = classify_cells_by_color(img, masks)

    # main.py: count(np.unique(masks))
    total_cells = count(np.unique(masks))

    return masks, flows, all_counts, total_cells
