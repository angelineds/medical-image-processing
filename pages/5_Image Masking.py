import streamlit as st
import numpy as np
from PIL import Image
from skimage import img_as_ubyte
from skimage.color import rgb2gray
from skimage import exposure   #untuk contrast
import scipy.ndimage as ndi 

st.set_page_config(
    layout="wide",
    page_title="Final Project"
)

menu = ["Masking", "Dilation and Erosion", "Opening and Closing"]

imgfile = st.file_uploader("Upload Image:", type=["png", "jpg", "jpeg"])
if "imgfile_state" not in st.session_state:
    st.session_state.imgfile_state = False
if imgfile or st.session_state.imgfile_state:
    st.session_state.imgfile_state = True

if imgfile is not None:
    img = Image.open(imgfile)
    img = np.array(img, dtype=np.uint8)

    gray_img = rgb2gray(img)
    gray_img = img_as_ubyte(gray_img)

    img_adapt = exposure.equalize_adapthist(gray_img, clip_limit=0.01)
    img_adapt = img_as_ubyte(img_adapt)

    hist = ndi.histogram(gray_img, min=0, max=255, bins=256)
    hist_adapt = ndi.histogram(img_adapt, min=0, max=255, bins=256)

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col2:
            st.markdown("<h4 style='text-align: center;'>Grayscaled Image </h4>", unsafe_allow_html=True)
            st.image(gray_img)
        with col3:
            st.markdown("<h4 style='text-align: center;'>AHE Image</h4>", unsafe_allow_html=True)
            st.image(img_adapt)
        col4, col5, col6 = st.columns(3)
        with col5:
            st.line_chart(hist)
        with col6:
            st.line_chart(hist_adapt)

    st.success("Based on the graph above, determine the range value of masking.")
    min_v = st.number_input("Minimum value:", 0, 255)
    max_v = st.number_input("Maximum value:", 0, 255)
    mask = (img_adapt >= min_v) & (img_adapt <= max_v)
    mask = mask*255                         #dikali satu utk convert "true-false" ke "1-0"

    choice = st.selectbox("Type of result to show:", menu)
    if choice == "Masking":
        imm_mask = np.where(mask, img_adapt, 0)
        hist_mask = ndi.histogram(imm_mask, min=1, max=255, bins=255)
        col7, col8 = st.columns(2)
        with col7:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col8:
            st.markdown("<h4 style='text-align: center;'>Masking Result </h4>", unsafe_allow_html=True)
            st.image(mask)
        st.line_chart(hist_mask)

    elif choice == "Dilation and Erosion":
        itr_dlt = st.slider("Iterations of dilation process: ", 1, 20)
        itr_ers = st.slider("Iterations of erosion process: ", 1, 20)

        dlt = ndi.binary_dilation(mask, iterations=itr_dlt)
        dlt = dlt*255
        ers = ndi.binary_erosion(mask, iterations=itr_ers)
        ers = ers*255
        col9, col10, col11 = st.columns(3)
        with col9:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(mask)
        with col10:
            st.markdown("<h4 style='text-align: center;'>Dilation Result </h4>", unsafe_allow_html=True)
            st.image(dlt)
        with col11:
            st.markdown("<h4 style='text-align: center;'>Erosion Result </h4>", unsafe_allow_html=True)
            st.image(ers)

    elif choice == "Opening and Closing":
        itr_open = st.slider("Iterations of opening process: ", 1, 20)
        itr_close = st.slider("Iterations of closing process: ", 1, 20)

        opening = ndi.binary_opening(mask, iterations=itr_open)
        opening = opening*255
        closing = ndi.binary_closing(mask, iterations=itr_close)
        closing = closing*255
        col9, col10, col11 = st.columns(3)
        with col9:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(mask)
        with col10:
            st.markdown("<h4 style='text-align: center;'>Opening Result </h4>", unsafe_allow_html=True)
            st.image(opening)
        with col11:
            st.markdown("<h4 style='text-align: center;'>Closing Result </h4>", unsafe_allow_html=True)
            st.image(closing)
