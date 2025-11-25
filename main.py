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
from cell_counting import count

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

    print("Red cells detected: " + str(count(red_ROIs)))
    print("Green cells detected: " + str(count(green_ROIs)))
    print("Blue cells detected: " + str(count(blue_ROIs)))

    display_results(imgs_clean_array, masks, flows)