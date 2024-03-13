import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_drawable_canvas import st_canvas
import requests
import random
import pandas as pd
import json
import requests
import random
import base64
from gtts import gTTS
import io
import math
from simplification.cutil import simplify_coords
import numpy as np

st.set_page_config(
            page_title="Game", # => Quick reference - Streamlit
            page_icon=":pencil:",
            layout="centered", # wide
            initial_sidebar_state="auto")

def autoplay_audio(audio):
    '''Function Purpose:
            The autoplay_audio function is designed to create an HTML audio player that plays audio automatically
            without requiring manual interaction (i.e., clicking the “play” button).
            It takes an audio bytes object as input.
        Function Implementation:
            data = audio.read(): Reads the audio bytes from the input audio object.
            b64 = base64.b64encode(data).decode(): Encodes the audio data using base64 encoding.
            md: Constructs an HTML snippet for the audio player.
            The <audio> tag includes the controls attribute (which displays audio controls like play, pause, and volume)
            and the autoplay="true" attribute (which ensures automatic playback).
            The src attribute specifies the audio source as a base64-encoded data URI.
            The type attribute indicates that the audio is in MP3 format.
            st.markdown(md, unsafe_allow_html=True): Displays the HTML snippet within the Streamlit app.
        Usage:
            You can call this function with an audio bytes object (e.g., generated using gTTS).
            It will render an audio player in your Streamlit app that plays the audio automatically.
    '''
    data = audio.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
    <audio controls autoplay="true">
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(
        md,
        unsafe_allow_html=True,
        )

def tts(word):
    '''
    Function Purpose:
        The tts function is designed to create a simple Streamlit app for text-to-speech (TTS) conversion.
        It allows the user to input a word or text, converts it to audio using gTTS, and plays it automatically.
    Function Implementation:
        st.title("Automatic Text-to-Speech Demo"): Sets the title of the Streamlit app.
        user_input = st.text_input("Enter a word:"): Creates a text input field where the user can enter a word or text.
        if user_input:: Checks if the user input is not empty and execure inner function play_word().
        tts = gTTS(text=user_input, lang="en", slow=False): Creates a gTTS object with the user input text and English language.
        audio_bytes = io.BytesIO(): Initializes an in-memory byte stream to store the audio data.
        tts.write_to_fp(audio_bytes): Writes the audio data to the byte stream.
        audio_bytes.seek(0): Resets the stream position to the beginning.
        autoplay_audio(audio_bytes): Calls the autoplay_audio function with the audio bytes.
    Usage:
        The user enters a word or text in the input field.
        The gTTS library converts the input to audio and stores it in the audio_bytes object.
        The autoplay_audio function plays the audio automatically.
    '''

    def play_word(user_input):
        tts = gTTS(text=user_input, lang="es", tld="es", slow=False)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        #st.audio(audio_bytes, format="audio/mp3", start_time=0)
        audio_bytes.seek(0)
        autoplay_audio(audio_bytes)

    play_word(word)

    # user_input = word

    # if user_input:
    #     play_word(user_input)

# # Resampling the drawing (all strokes) based on time
# def resampling_time_post(json_drawing: json, step: int = 1) -> dict:
#     lst_strokes = json.loads(json_drawing)['drawing']
#     lst_strokes_resampled = []
#     for stroke in lst_strokes:
#         stroke_resampled = []
#         stroke_resampled.append(stroke[0][::step]) # resampled xs
#         stroke_resampled.append(stroke[1][::step]) # resampled ys
#         lst_strokes_resampled.append(stroke_resampled)
#     dict_strokes_resampled = {'drawing': lst_strokes_resampled}
#     return dict_strokes_resampled


######################################################
#### Resampling the raw data using method provided on kaggle
#### https://www.kaggle.com/code/inversion/getting-started-viewing-quick-draw-doodles-etc?scriptVersionId=6015273&cellId=11
######################################################

def resample(x, y, spacing=1.0):
    output = []
    n = len(x)
    px = x[0]
    py = y[0]
    cumlen = 0
    pcumlen = 0
    offset = 0
    for i in range(1, n):
        cx = x[i]
        cy = y[i]
        dx = cx - px
        dy = cy - py
        curlen = math.sqrt(dx*dx + dy*dy)
        cumlen += curlen
        while offset < cumlen:
            t = (offset - pcumlen) / curlen
            invt = 1 - t
            tx = px * invt + cx * t
            ty = py * invt + cy * t
            output.append((tx, ty))
            offset += spacing
        pcumlen = cumlen
        px = cx
        py = cy
    output.append((x[-1], y[-1]))
    return output

'''
###### !!THIS IS A MASSIVE QUACK!! ######
# Function name should be 'normalize_resample_simplify' - using old function name to ensure comptability
'''
def resampling_time_post(json_drawing: json, epsilon=1.0, resample_spacing=1.0):
    strokes = json.loads(json_drawing)['drawing']

    if len(strokes) == 0:
        raise ValueError('empty image')

    # find min and max
    amin = None
    amax = None
    for x, y in strokes:
        cur_min = [np.min(x), np.min(y)]
        cur_max = [np.max(x), np.max(y)]
        amin = cur_min if amin is None else np.min([amin, cur_min], axis=0)
        amax = cur_max if amax is None else np.max([amax, cur_max], axis=0)

    # drop any drawings that are linear along one axis
    arange = np.array(amax) - np.array(amin)
    if np.min(arange) == 0:
        raise ValueError('bad range of values')

    arange = np.max(arange)
    output = []
    for x, y in strokes:
        xy = np.array([x, y], dtype=float).T
        xy -= amin
        xy *= 255.
        xy /= arange
        resampled = resample(xy[:, 0], xy[:, 1], resample_spacing)
        simplified = simplify_coords(resampled, epsilon)
        xy = np.around(simplified).astype(np.uint8)
        output.append(xy.T.tolist())

    dict_strokes_resampled = {'drawing': output}
    return dict_strokes_resampled

######################################################
######################################################


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

if 'random_class' not in st.session_state:
    random_class = random.choice(list(reversed_dict.values()))
    st.session_state['random_class'] = random_class

else:
    random_class = st.session_state['random_class']

st.header(f"Please draw {random_class}")

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

def another_game():
    col1, col2, col3 = st.columns(3)

    col1.write("")  # Empty column
    col2.button("   Click here to play again")
    col3.write("")  # Empty column

#trying to add in prediction
predict_url = "http://localhost:8080/predict"

post_dict = resampling_time_post(json_drawing)

if len(json_drawing) > 15:

    res = requests.post(url=predict_url, json=post_dict, headers={'Content-Type':'application/json'})
    #this request returns a dictionary with the array of percentages and the hgihest class
    res = res.content

#this is the predicted class
    class_pred = reversed_dict[int(eval(res.decode())['prediction'])]

    if class_pred != random_class:
        st.write(reversed_dict[int(eval(res.decode())['prediction'])])
        tts(reversed_dict[int(eval(res.decode())['prediction'])])
        st.write("You made a wrong prediction, keep drawing")
    else: # do we wnat
        st.write(reversed_dict[int(eval(res.decode())['prediction'])])
        st.write("You got it!")

add_vertical_space(10)

image1 = 'https://storage.googleapis.com/pictionary-ai-website-bucket/preview.jpg'
st.image(image1, width=710)
