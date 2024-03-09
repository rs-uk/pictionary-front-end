import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
import requests
from params import *
import matplotlib.pyplot as plt


# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=3, # this can be adjusted during testing
    stroke_color='#000000', # we only want to draw in black
    background_color='#ffffff', # we set the background color to white
    background_image=None, # we do not need a backgorund image on the canvas
    update_streamlit=True, # we want the output to be live
    height=400,
    width=600,
    drawing_mode='freedraw', # we only want that option from st_canvas
    point_display_radius=0, # we only care about freedraw mode here
    key="canvas"
)


# Show the outputs on streamlit
if canvas_result.json_data is not None:
    # need to convert obj to str because of PyArrow
    objects = pd.json_normalize(canvas_result.json_data["objects"])
    for col in objects.select_dtypes(include=['object']).columns:
        objects[col] = objects[col].astype("str")
    # st.dataframe(objects)


# Show the resulting JSON on streamlit
# st.json(canvas_result.json_data['objects'])


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
def resampling_time_post(json_drawing: json, step: int = 5) -> dict:
    lst_strokes = json.loads(json_drawing)['drawing']
    lst_strokes_resampled = []
    for stroke in lst_strokes:
        stroke_resampled = []
        stroke_resampled.append(stroke[0][::step]) # resampled xs
        stroke_resampled.append(stroke[1][::step]) # resampled ys
        lst_strokes_resampled.append(stroke_resampled)
    dict_strokes_resampled = {'drawing': lst_strokes_resampled}
    return dict_strokes_resampled


# Pass the JSON resampled drawing to the API
api_url = f"{base_url}/api"
upload = requests.post(api_url, json=resampling_time_post(json_drawing)
                        ,headers={'Content-Type':'application/json'})
st.write(upload.content)


# Show the JSON drawing in streamlit (truncating coords lists to 101-length is
# only on streamlit display, tested by file-saving below)
# st.text('JSON of the drawing:')
# st.json(json_drawing)


# Write the dict to a JSON file for testing
# Not writing json_drawing as this is a string
# file_index = 5
# if outputs is not None:
#     with open(f"drawing_input_test{file_index}.json", 'w') as file:
#         json.dump(dict_strokes, file)
#     with open(f"drawing_input_resampled_post_test{file_index}.json", 'w') as file:
#         json.dump(json.loads(resampling_time_post(json_drawing)), file)


# Show the end drawing in streamlit
# if canvas_result.image_data is not None:
#     st.image(canvas_result.image_data)


# Resampling the drawing (all strokes) based on distance
# def resampling_distance_post(json_drawing: json, step: int = 5) -> json:
#     lst_strokes = json.loads(json_drawing)['drawing']
#     lst_strokes_resampled = []
#     for stroke in lst_strokes:
#         stroke_resampled = []
#         # We keep the first point of the stroke
#         stroke_resampled.append([stroke[0][0]])
#         stroke_resampled.append([stroke[1][0]])
#         # We scroll through the points of the stroke and keep points which are
#         # at least 'step' pixels apart
#         if len(stroke[0]) > 2:
#             for i in range(1, len(stroke[0])-1):
#                 if ((stroke[0][i] - stroke_resampled[0][-1])**2 + (stroke[1][i] - stroke_resampled[1][-1])**2)**0.5 >= step:
#                     # If the next point is far enough we append it to the resampled stroke
#                     stroke_resampled[0].append(stroke[0][i])
#                     stroke_resampled[1].append(stroke[1][i])
#         # We then append the last point of the stroke no matter its distance to the previous sampled point
#         stroke_resampled[0].append(stroke[0][-1])
#         stroke_resampled[1].append(stroke[1][-1])
#         lst_strokes_resampled.append(stroke_resampled)
#     dict_strokes_resampled = {'drawing': lst_strokes_resampled}
#     return json.dumps(dict_strokes_resampled)


# Show the JSON resampled drawing in streamlit (truncating coords lists to 101-length
# is only on streamlit display, tested by file-saving below)
if outputs is not None:
    st.text('JSON of the resampled drawing:')
    st.json(resampling_time_post(json_drawing, step=resampling_time_step))


# Show the resampled drawing in streamlit
# Create the figure and flip the y axis (drawings captured from top-left corner)
plt_drawing_resampled = plt.figure(figsize=(8, 6))
plt.gca().invert_yaxis()
plt.axis('off')
# Grab the resampled drawing's JSON
json_drawing = resampling_time_post(json_drawing, step=resampling_time_step)
# Iterate through the strokes and add segments to the figure
for stroke in json_drawing['drawing']:
    xs = stroke[0]
    ys = stroke[1]
    # Connect the points with lines
    for i in range(len(xs) - 1):
        plt.plot([xs[i], xs[i + 1]], [ys[i], ys[i + 1]], color='black')
# Display in streamlit
if outputs is not None:
    st.text('Resampled drawing:')
    st.pyplot(plt_drawing_resampled)


# Resampling the live drawing (for each new point) based on time
def resampling_time_live(json_drawing: json, step: int = 5) -> json:
    pass # TODO
