import streamlit as st
import time
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.let_it_rain import rain
import requests
import random

import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
import requests
import numpy as np


# from params import *

import matplotlib.pyplot as plt
import random

st.set_page_config(
            page_title="Game", # => Quick reference - Streamlit
            page_icon=":pencil:",
            layout="centered", # wide
            initial_sidebar_state="auto")

# Resampling the drawing (all strokes) based on time
def resampling_time_post(json_drawing: json, step: int = 1) -> dict:
    lst_strokes = json.loads(json_drawing)['drawing']
    lst_strokes_resampled = []
    for stroke in lst_strokes:
        stroke_resampled = []
        stroke_resampled.append(stroke[0][::step]) # resampled xs
        stroke_resampled.append(stroke[1][::step]) # resampled ys
        lst_strokes_resampled.append(stroke_resampled)
    dict_strokes_resampled = {'drawing': lst_strokes_resampled}
    return dict_strokes_resampled


st.title('Pictionary :blue[AI] :pencil:')

st.markdown("We will randomly choose one out of 50 images for you to draw in 20 seconds...")
add_vertical_space(3)


dictionary = {"aircraft carrier": 0, "arm": 1, "asparagus": 2, "backpack": 3,
              "banana": 4, "basketball": 5, "bottlecap": 6, "bread": 7, "broom": 8,
              "bulldozer": 9, "butterfly": 10, "camel": 11, "canoe": 12, "chair": 13,
              "compass": 14, "cookie": 15, "drums": 16, "eyeglasses": 17, "face": 18,
              "fan": 19, "fence": 20, "fish": 21, "flying saucer": 22, "grapes": 23,
              "hand": 24, "hat": 25, "horse": 26, "light bulb": 27, "lighthouse": 28,
              "line": 29, "marker": 30, "mountain": 31, "mouse": 32, "parachute": 33,
              "passport": 34, "pliers": 35, "potato": 36, "sea turtle": 37, "snowflake": 38,
              "spider": 39, "square": 40, "steak": 41, "swing set": 42, "sword": 43,
              "telephone": 44, "television": 45, "tooth": 46, "traffic light": 47, "trumpet": 48, "violin": 49}
reversed_dict = {v: k for k, v in dictionary.items()}
#reversing dictionary

#this will give a random class

if 'random_class' not in st.session_state:
    random_class = random.choice(list(reversed_dict.values()))
    st.session_state['random_class'] = random_class

else:
    random_class = st.session_state['random_class']

st.header(f"Please draw a {random_class}")

def countdown_with_progress():

    canvas_result = st_canvas(fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=3, # this can be adjusted during testing
    stroke_color='#000000', # we only want to draw in black
    background_color='#FFFFFF', # we set the background color to white
    background_image=None, # we do not need a background image on the canvas
    update_streamlit=True, # we want the output to be live
    height=400,
    width=600,
    drawing_mode='freedraw', # we only want that option from st_canvas
    point_display_radius=0, # we only care about freedraw mode here
    key="canvas")

    # Show the outputs on streamlit
    if canvas_result.json_data is not None:
        # need to convert obj to str because of PyArrow
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.select_dtypes(include=['object']).columns:
            objects[col] = objects[col].astype("str")
        # st.dataframe(objects)
    # Show the resulting JSON on streamlit
    #st.json(canvas_result.json_data['objects'])
    # Extract the drawing and process to match the expected format
    outputs = canvas_result.json_data['objects']
    lst_strokes = []
    # Going stroke by stroke:
    for stroke in outputs:
        stroke = stroke['path'] # we only want the 'path' of the stroke in the JSON
        xs = []
        ys = []
        for step in stroke: # the steps are either one or two points
            # Build list of xs and ys.
            # Only 1 point for the first and last steps of each stroke ('M' and 'L')
            if step[0] == 'M' or step[0] == 'L':
                xs.append(int(step[1]))
                ys.append(int(step[2]))
            # 2 points for the intermediary steps of each stroke ('Q')
            elif step[0] == 'Q':
                # Adding both sets of coords to x and y
                xs.append(int(step[1]))
                xs.append(int(step[3]))
                ys.append(int(step[2]))
                ys.append(int(step[4]))
        lst_strokes.append([xs, ys])
    dict_strokes = {'drawing': lst_strokes}
    # Convert the dict to JSON
    json_drawing = json.dumps(dict_strokes)
    # Resampling the drawing (all strokes) based on time

    return json_drawing

json_drawing = countdown_with_progress()


# st.write(json_drawing)

def another_game():
    col1, col2, col3 = st.columns(3)

    col1.write("")  # Empty column
    col2.button("   Click here to play again")
    col3.write("")  # Empty column


#trying to add in prediction
predict_url = "http://localhost:8080/predict"

post_dict = resampling_time_post(json_drawing)

if len(json_drawing) > 15:

    # st.write("You drew a line")

    res = requests.post(url=predict_url, json=post_dict, headers={'Content-Type':'application/json'})
    #this request returns a dictionary with the array of percentages and the hgihest class
    res = res.content

#this is the predicted class
    class_pred = reversed_dict[int(eval(res.decode())['prediction'])]

    if class_pred != random_class:
        st.write(reversed_dict[int(eval(res.decode())['prediction'])])
        st.write((eval(res.decode())['prob']))
        st.write(eval(res.decode())['probabilities'])
        st.write("You made a wrong prediction, keep drawing")
    else: # do we wnat
        st.write(reversed_dict[int(eval(res.decode())['prediction'])])
        st.write("You got it!")

add_vertical_space(10)

image1 = 'https://storage.googleapis.com/pictionary-ai-website-bucket/preview.jpg'
st.image(image1, width=710)
