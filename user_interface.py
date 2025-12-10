import streamlit as st
import numpy as np
import cv2

from cell_identification import (
    split_channels,
    clean,
    create_model,
    segment,
    extract_ROI,
)
from cell_counting import count

st.title("Tezak Cell Counter")

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded:
    # Convert uploaded file into an OpenCV image
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(img, caption="Original Image", use_column_width=True)

    if st.button("Run Cell Counting"):
        with st.spinner("Identifying cells..."):

            # 1. Split into color channels using your backend
            #    split_channels is defined in cell_identification.py
            b, g, r = split_channels(img)

            # 2. Clean / preprocess channels using your backend
            #    clean is defined in cell_identification.py
            imgs_clean_array = clean(r, g, b)

            # 3. Create Cellpose model using your backend
            #    create_model is defined in cell_identification.py
            model = create_model()

            # 4. Run segmentation using your backend
            #    segment is defined in cell_identification.py
            masks, flows, styles = segment(model, imgs_clean_array)

            # 5. Extract ROIs for each color channel using your backend
            #    extract_ROI is defined in cell_identification.py
            red_ROIs = extract_ROI('red', masks)
            green_ROIs = extract_ROI('green', masks)
            blue_ROIs = extract_ROI('blue', masks)

            # 6. Count cells using your backend
            #    count is defined in cell_counting.py
            red_count = count(red_ROIs)
            green_count = count(green_ROIs)
            blue_count = count(blue_ROIs)

        st.subheader("Cell Counts")
        st.write(f"**Red cells detected:** {red_count}")
        st.write(f"**Green cells detected:** {green_count}")
        st.write(f"**Blue cells detected:** {blue_count}")

        # (Optional) You can later add visualization of masks here if you want
        # using imgs_clean_array, masks, and flows
