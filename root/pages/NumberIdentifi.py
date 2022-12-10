import joblib
import numpy as np
import streamlit as st
import cv2
from streamlit_drawable_canvas import st_canvas
import streamlit_nested_layout
from hydralit import HydraHeadApp

SIZE = 192
drawing_mode =  "freedraw"
stroke_color = "#FFFFFF"
bg_color = "#000000"
realtime_update =  True

class NumberIdentifi(HydraHeadApp):

    def run(self):
        st.title("Nhận diện chữ số với KNN")
        st.header("Vẽ chữ số từ 0 đến 9:")

        container1 = st.container()
        with container1.container():
            container2 = st.empty()
            with container2.container():
                temp1,temp2 = st.columns(2)
                with temp1:
                    stroke_width = st.slider("Nét vẽ: ", 1, 25, 18)
        with container1.container():
            col1,col2,col3,col4 = st.columns([1,2,1,5])
            with col1:
                # Create a canvas component
                canvas_result = st_canvas(
                    fill_color="#000000",  # Fixed fill color with some opacity
                    stroke_width = stroke_width,
                    stroke_color = stroke_color,
                    background_color = bg_color,
                    update_streamlit = realtime_update,
                    height = SIZE,
                    width = SIZE,
                    drawing_mode = drawing_mode,
                    key="canvas",
                )
            with col2:
                st.write("=====================================>")
                page_bg = f"""
                <style>
                div[data-testid="stHorizontalBlock"] {{
                    align-items: center;
                }}
                [title="streamlit_drawable_canvas.st_canvas"] > #document.html:root{{
                    --background-color: none;                
                }}
                </style>
                """
                st.markdown(page_bg, unsafe_allow_html=True)

            with col3:
                # Do something interesting with the image data and paths
                if canvas_result.image_data is not None:
                    img = cv2.resize(canvas_result.image_data.astype(np.uint8),(28,28),interpolation=cv2.IMREAD_GRAYSCALE)
                    rescaled = cv2.resize(img, (SIZE, SIZE), interpolation=cv2.INTER_NEAREST)
                    st.image(rescaled)
            with col4:
                if st.button("Predict"):
                    RESHAPED = 784
                    knn = joblib.load('.\\root\\pages\\NumberRecognition\\knn_mnist.pkl')
                    test_x = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    val = knn.predict(test_x.reshape(1,RESHAPED))
                    font_size = f"""
                    <style>
                    code {{
                        font-size: 3rem !important;
                    }}
                    </style>
                    """
                    st.markdown(font_size,unsafe_allow_html=True)
                    st.write(val[0])