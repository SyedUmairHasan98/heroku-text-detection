import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import requests
import time
import os

st.title("Text Detection")
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            .styles_stateContainer__29Rp6 {visibility: hidden; display: none;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def detect():
    flag = False
    # Specify canvas parameters in application
    stroke_width = st.sidebar.slider("Stroke width: ", 5, 20, 6)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ","#ffffff")
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        #background_color="#eee",
        background_color="black",
        height=250,
        drawing_mode='freedraw',
        display_toolbar=st.sidebar.checkbox("Display toolbar", True)
    )

    # Do something interesting with the image data and paths
    if st.button('Submit'):
        if canvas_result.image_data is not None:
            cv2.imwrite(f"img.jpg",  canvas_result.image_data)
            flag = True


    if flag == True:
        with st.spinner('Working on it'):
          with open('img.jpg', 'rb') as f:
            data = f.read()
          r = requests.post(os.environ["endpoint"],data=data,headers={"Ocp-Apim-Subscription-Key":os.environ["key"],"Content-Type": "application/octet-stream"})
          time.sleep(3)
          r2 = requests.get(r.headers['Operation-Location'],headers={"Ocp-Apim-Subscription-Key":os.environ["key"]})
          my_dict = {}
        for line in r2.json()['analyzeResult']['readResults'][0]['lines']:
          st.markdown(f"<h1 style='text-align:center;font-family:cursive;'>{line['text']}</h1>",unsafe_allow_html=True)
          for word in line['words']:
            my_dict[word['text']] = word['confidence']
        for key in my_dict:
            st.metric(label='',value=f"{key}", delta=f"{my_dict[key]*100} %")
            st.progress(my_dict[key])
        flag = False


detect()
