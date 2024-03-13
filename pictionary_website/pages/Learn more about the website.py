import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(
            page_title="Project information", # => Quick reference - Streamlit
            page_icon=":pencil:",
            layout="centered", # wide
            initial_sidebar_state="auto")

add_vertical_space(3)
st.markdown("<h2 style='font-size: 1.5em; text-decoration: underline;'>Where to find the data</h2>", unsafe_allow_html=True)
st.markdown("* Click below to visualize all of the previous drawing data that Google collected from their model")
st.link_button(":red[Previous examples]", "https://quickdraw.withgoogle.com/data")

add_vertical_space(1)
st.markdown("* Click below to access all of the simplfied data that we used")
st.link_button(":red[Simplified data]", "https://console.cloud.google.com/storage/browser/quickdraw_dataset/full/simplified")

add_vertical_space(2)
st.markdown("<h2 style='font-size: 1.5em; text-decoration: underline;'>How This Project Was Created</h2>", unsafe_allow_html=True)
image_raw = "https://storage.googleapis.com/pictionary-ai-website-bucket/raw_alarm_example.jpg"
image_simp = "https://storage.googleapis.com/pictionary-ai-website-bucket/simplified_alarm.jpg"
add_vertical_space(1)
st.markdown(":red[Preprocessing]")

st.markdown(" - There were four different formats of data available for us to use. We chose to use the simplified data, which contained 345 different drawings and 50 million different drawings in totality")
st.markdown('- We visualised the drawings taken from the raw data set, which contained a vast sum of points on each drawing')

col1, col2 = st.columns(2)

col1.image(image_raw, width=412)
col2.image(image_simp, width=417)

st.markdown('* As shown by the images above, the simplified data set contained far fewer points when visualised, requiring far less computing power whilst still retaining a comprehendible image')
st.markdown('- We created a function that allowed us to process the simplified data set, returning an array and a class name (which was the drawing to for the computer to guess)')
st.markdown('- We then created a function that returned a dictionary of the drawings, containing the class, the individual image id and the delta data that we need.')
st.markdown('- Then we applied padding, one hot encoded and shuffled our data set.')
add_vertical_space(10)
st.markdown(':red[Model]')
add_vertical_space(1)
st.markdown('* We used a bidirectional Long Short-Term-Memory (LSTM) model that achieved  X %age accuracy across our data set')
st.markdown("* This model is a type of reccurent neural network (RNN) that processes sequential data in both forwards and backwards directions")
st.markdown('* This type of model was chosen to appropriately add weight to the beginning and ends of the drawings, as we thought these were the most important periods')
image_model = "https://storage.googleapis.com/pictionary-ai-website-bucket/model.jpg"
st.image(image_model)

image_simplified = "https://storage.googleapis.com/pictionary-ai-website-bucket/simplified.jpg"
add_vertical_space(3)
st.markdown("* Below you can see a more simple visualisation of what's at play here")
st.image(image_simplified)
st.markdown("* An additional benefit of using a Bidirectional LSTM is that it has very flexible architecture, and is easily customisable through adding additional layers, uch as convolutional or attention layers, to improve performance.")
st.markdown("* We trained the model on 50 different classes of drawings")
add_vertical_space(5)

st.markdown(':red[Front End]')
add_vertical_space(1)
st.markdown('* We managed to find a model where you can draw with a mouse on a canvas on streamlit, and take that data as our input in the same format that we have done all of the preprocessing, trained and tested our drawings on.')
st.markdown('* - This input contains the delta of X and y as points from the drawing, and the start and stop of the stroke as the third feature.')
st.markdown('* - The canvas is very customisable and allows  us to change things like the colour of the marker, to make the website more fun and interactive')
add_vertical_space(10)
image1 = 'https://storage.googleapis.com/pictionary-ai-website-bucket/preview.jpg'
st.image(image1, width=730)
