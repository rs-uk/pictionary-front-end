import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas


# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=3, # this can be adjusted during testing
    stroke_color='#000000', # we only want to draw in black
    background_color='#ffffff', # we set the background color of the canvas to white
    background_image=None, # we do not need a backgorund image on the canvas
    update_streamlit=True, # we want the output to be live
    height=400,
    width=600,
    drawing_mode='freedraw', # we only want that option from st_canvas
    point_display_radius=0, # we only care about freedraw mode so no need for this
    key="canvas",
)

# Show the outputs
if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"]) # need to convert obj to str because PyArrow
    for col in objects.select_dtypes(include=['object']).columns:
        objects[col] = objects[col].astype("str")
    st.dataframe(objects)


# Show the end drawing
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data)
