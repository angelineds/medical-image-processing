import streamlit as st
import numpy as np
import scipy.ndimage as ndi
from PIL import Image
from Imaging_017 import histogram_equalization, adaptive_HE, contrast_stretching

st.set_page_config(
    layout="wide",
    page_title="Final Project"
)

menu = ["Histogram Equalization", "Adaptive Histogram Equalization", "Contrast Stretching"]
choice = st.selectbox("Type of image enhancement:", menu)

imgfile = st.file_uploader("Upload Image:", type=["png", "jpg", "jpeg"])
if "imgfile_state" not in st.session_state:
    st.session_state.imgfile_state = False
if imgfile or st.session_state.imgfile_state:
    st.session_state.imgfile_state = True

if imgfile is not None:
    img = Image.open(imgfile)
    img = np.array(img, dtype=np.uint8)

    if choice == "Histogram Equalization":
        graph, HE, HE_graph = histogram_equalization(img)
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
                st.image(img)
            with col2:
                st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
                st.image(HE)
            col3, col4 = st.columns(2)
            with col3:
                st.line_chart(graph)
            with col4:
                st.line_chart(HE_graph)

    elif choice == "Adaptive Histogram Equalization":
        clip = st.slider("Clip limit: ", 0.0, 10.0, 0.04)
        if clip:
            AHE = adaptive_HE(img, clip)
            col5, col6 = st.columns(2)
            with col5:
                st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
                st.image(img)
            with col6:
                st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
                st.image(AHE, caption=f"Clip limit: {clip}")          

    elif choice == "Contrast Stretching":
        graph = ndi.histogram(img, min=0, max=255, bins=256)
        min = st.number_input('Minimum value:', 1, 256, 10)
        max = st.number_input('Maximum value: ', 1, 256, 250)
        CS, CS_graph = contrast_stretching(img, 0, 255, min, max)
        with st.container():
            col7, col8 = st.columns(2)
            with col7:
                st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
                st.image(img)
            with col8:
                st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
                st.image(CS)
            col9, col10 = st.columns(2)
            with col9:
                st.line_chart(graph)
            with col10:
                st.line_chart(CS_graph)