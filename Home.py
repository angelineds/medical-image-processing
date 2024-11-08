import streamlit as st
from PIL import Image

st.set_page_config(
    layout="wide",
    page_title="Final Project"
)

def main():
    st.caption("\n\n | Angeline Dwi Sanjaya")
    st.header("Medical Imaging Project: Image Processing")

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(Image.open("./assets/Image Enhancement.png"))
        with col2:
            st.image(Image.open("./assets/Image Filtering.png"))
        with col3:
            st.image(Image.open("./assets/Performance Evaluation.png"))
 
        col4, col5, col6 = st.columns(3)
        with col4:
            st.image(Image.open("./assets/Edge Detection.png"))
        with col5:
            st.image(Image.open("./assets/Masking.png"))

if __name__ == '__main__':
    main()
