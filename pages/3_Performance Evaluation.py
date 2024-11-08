import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
from Imaging_017 import evaluation_ENL, evaluation_PSNR, evaluation_NM

st.set_page_config(
    layout="wide",
    page_title="Final Project"
)

menu = ["Equivalent Number of Looks (ENL)", "Peak Signal-to-Noise Ratio (PSNR)", "Normalized Mean (NM)"]
choice = st.selectbox("Type of performance evaluation for imaging:", menu)

st.warning("Please make sure that The original image was the first image that was uploaded.")
pro_img = st.file_uploader("Upload image(s) to compare:", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
if "pro_img_state" not in st.session_state:
    st.session_state.pro_img_state = False
if pro_img or st.session_state.pro_img_state:
    st.session_state.pro_img_state = True

if pro_img is not None:
    item = {}
    for pro in pro_img:
        img = Image.open(pro)
        img = np.array(img, dtype=np.uint8)

        if choice == "Equivalent Number of Looks (ENL)":
            for i in range(len(pro_img)):
                item[pro_img[i].name] = evaluation_ENL(pro_img[i])

        elif choice == "Peak Signal-to-Noise Ratio (PSNR)":
            for i in range(1, len(pro_img)):
                item[pro_img[i].name] = evaluation_PSNR(pro_img[0], pro_img[i])

        elif choice == "Normalized Mean (NM)":
            for i in range(1, len(pro_img)):
                item[pro_img[i].name] = evaluation_NM(pro_img[0], pro_img[i])
    st.write(item)
