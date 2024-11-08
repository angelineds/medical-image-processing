import streamlit as st
import numpy as np
from PIL import Image
from Imaging_017 import mean_filter
import scipy.ndimage as ndi   

st.set_page_config(
    layout="wide",
    page_title="Final Project"
)

menu = ["Mean Filter", "Max-Min Filter", "Gaussian Filter", "Median Filter"]
choice = st.selectbox("Type of filter:", menu)

imgfile = st.file_uploader("Upload Image:", type=["png", "jpg", "jpeg"])
if "imgfile_state" not in st.session_state:
    st.session_state.imgfile_state = False
if imgfile or st.session_state.imgfile_state:
    st.session_state.imgfile_state = True

if imgfile is not None:
    img = Image.open(imgfile)
    img = np.array(img, dtype=np.uint8)

    if choice == "Mean Filter":
        kernel = st.radio("Kernel size: ", ("3x3", "5x5", "7x7"), horizontal=True)
        if kernel == "3x3":
            mean_img = mean_filter(img, 9)
        elif kernel == "5x5":
            mean_img = mean_filter(img, 25)
        elif kernel == "7x7":
            mean_img = mean_filter(img, 49)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col2:
            st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
            st.image(mean_img)

    elif choice == "Max-Min Filter":
        max_k = st.slider("Kernel size for maximum filter: ", 1, 20)
        max_img = ndi.maximum_filter(img, size=max_k)
        min_k = st.slider("Kernel size for minimum filter: ", 1, 20)
        min_img = ndi.minimum_filter(img, size=min_k)

        col3, col4, col5 = st.columns(3)
        with col3:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col4:
            st.markdown("<h4 style='text-align: center;'>Maximum Filter </h4>", unsafe_allow_html=True)
            st.image(max_img)      
        with col5:
            st.markdown("<h4 style='text-align: center;'>Mininum Filter (Result) </h4>", unsafe_allow_html=True)
            st.image(min_img)    

    elif choice == "Gaussian Filter":
        s_value = st.slider("Sigma value: ", 0.0, 20.0)
        gauss_img = ndi.gaussian_filter(img, sigma=s_value)

        col6, col7 = st.columns(2)
        with col6:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col7:
            st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
            st.image(gauss_img)

    elif choice == "Median Filter":
        kernel = st.radio("Kernel size: ", ("3x3", "5x5", "7x7", "11x11"), horizontal=True)
        if kernel == "3x3":
            med_img = ndi.median_filter(img, size=3)
        elif kernel == "5x5":
            med_img = ndi.median_filter(img, size=5)
        elif kernel == "7x7":
            med_img = ndi.median_filter(img, size=7)
        elif kernel == "11x11":
            med_img = ndi.median_filter(img, size=11)

        col8, col9 = st.columns(2)
        with col8:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col9:
            st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
            st.image(med_img)