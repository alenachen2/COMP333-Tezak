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

if __name__ == "__main__":
    img_path = get_file_path()
    img = cv2.imread(img_path).copy()

    b, g, r = split_channels(img)
    imgs_clean_array = clean(r, g, b)

    with yaspin(text="Identifying cells...", color="yellow") as spinner:
        model = create_model()
        masks, flows, styles = segment(model, imgs_clean_array)

    red_ROIs = extract_ROI('red', masks)
    green_ROIs = extract_ROI('green', masks)
    blue_ROIs = extract_ROI('blue', masks)

    print(f"Red cells detected: {len(red_ROIs) - 1}"   
        f"\nGreen cells detected: {len(green_ROIs) - 1}"   
        f"\nBlue of cells detected: {len(blue_ROIs) - 1}") 

    display_results(imgs_clean_array, masks, flows)