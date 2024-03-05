import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json


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


# Show the resulting JSON
st.json(canvas_result.json_data['objects'])
# st.json(canvas_result.json_data)
#

# Extract the drawing and process to match the expected format
outputs = canvas_result.json_data['objects']
lst_strokes = []
# Going stroke by stroke:
for stroke_nb in range(len(outputs)): # the stroke itself is a 'path' in the JSON
    stroke = outputs[stroke_nb]['path']
    xs = []
    ys = []
    for point_nb in range(len(stroke)):
        # Build list of xs and ys.
        # For the first and last points of each stroke ('M' and 'L') there is only one set of coords.
        if stroke[point_nb][0] == 'M' or stroke[point_nb][0] == 'L':
            xs.append(int(stroke[point_nb][1]))
            ys.append(int(stroke[point_nb][2]))
        # For the intermediary points of each stroke ('Q') there are two sets of coords.
        elif stroke[point_nb][0] == 'Q':
            # Adding both sets of coords to x and y
            xs.append(int(stroke[point_nb][1]))
            xs.append(int(stroke[point_nb][3]))
            ys.append(int(stroke[point_nb][2]))
            ys.append(int(stroke[point_nb][4]))
    lst_strokes.append([xs, ys])

dict_strokes = {'drawing': lst_strokes}

# Convert the dict to JSON
json_drawing = json.dumps(dict_strokes)

# Show the JSON drawing in streamlit
st.text('JSON of the drawing:')
st.json(json_drawing)

# Write the dict to a JSON file for testing
# Not writing json_drawing as this is a string
# -- truncating coords lists to 101-length is only on streamlit --
if outputs is not None:
    with open('drawing_input_test3.json', 'w') as file:
        json.dump(dict_strokes, file)

# Show the end drawing
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data)
