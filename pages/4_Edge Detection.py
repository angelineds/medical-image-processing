import streamlit as st
import numpy as np
from PIL import Image
import cv2
from Imaging_017 import edgedetect_derivate, edgedetection_sobelprewitt, edgedetection_robert, edgedetection_laplacian

st.set_page_config(
    layout="wide",
    page_title="Final Project"
)

menu = ["Derivative Filters", "Sobel Operator", "Prewitt Operator", "Robert Operator", "Laplacian Operator", "Canny Detector"]
choice = st.selectbox("Type of edge detector:", menu)

imgfile = st.file_uploader("Upload Image:", type=["png", "jpg", "jpeg"])
if "imgfile_state" not in st.session_state:
    st.session_state.imgfile_state = False
if imgfile or st.session_state.imgfile_state:
    st.session_state.imgfile_state = True

if imgfile is not None:
    img = Image.open(imgfile)
    img = np.array(img, dtype=np.uint8)

    if choice == "Derivative Filters":
        deriv_img = edgedetect_derivate(img)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col2:
            st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
            st.image(deriv_img)

    elif choice == "Sobel Operator":
        sobelhorz = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        sobelvert = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])

        sobel_img = edgedetection_sobelprewitt(img, sobelhorz, sobelvert)
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col4:
            st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
            st.image(sobel_img)  

    elif choice == "Prewitt Operator":
        prewitthorz = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
        prewittvert = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])

        prewitt_img = edgedetection_sobelprewitt(img, prewitthorz, prewittvert)
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col6:
            st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
            st.image(prewitt_img) 

    elif choice == "Robert Operator":
        robert_img = edgedetection_robert(img)
        col7, col8 = st.columns(2)
        with col7:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col8:
            st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
            st.image(robert_img)  

    elif choice == "Laplacian Operator":
        st.warning("Please only input positive and odd number for both of the kernel size.")
        gauss_k = st.number_input("Kernel size of gaussian filter:", 1, 15)
        lapl_k = st.number_input("Kernel size for laplacian operator:", 1, 15)

        laplacian_img = edgedetection_laplacian(img, gauss_k, lapl_k)
        col9, col10 = st.columns(2)
        with col9:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col10:
            st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
            st.image(laplacian_img)  

    elif choice == "Canny Detector":
        lower = st.slider("Lower value:", 0, 255)
        upper = st.slider("Upper value:", 0, 255)

        canny_img = cv2.Canny(img, lower, upper)
        col11, col12 = st.columns(2)
        with col11:
            st.markdown("<h4 style='text-align: center;'>Original Image </h4>", unsafe_allow_html=True)
            st.image(img)
        with col12:
            st.markdown("<h4 style='text-align: center;'>Processed Image </h4>", unsafe_allow_html=True)
            st.image(canny_img)  