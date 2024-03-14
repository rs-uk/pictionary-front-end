import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

bucket_name = "pictionary-ai-website-bucket"
image_path = 'https://storage.googleapis.com/pictionary-ai-website-bucket/pictionary_ai.jpg'
st.set_page_config(
            page_title="Homepage", # => Quick reference - Streamlit
            page_icon=":pencil:",
            layout="centered", # wide
            initial_sidebar_state="auto")

st.markdown("<h1 style='text-align: center;'>Pictionary AI</h1>", unsafe_allow_html=True) #centralised title

st.image(image_path, use_column_width=True) #pictionary ai logo image

st.markdown("<h1 style='text-align: center; font-weight: normal;font-size: 22px;'>Welcome to Pictionary AI, the transformative new website that can predict your drawings!</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-weight: normal; font-size: 14px;'>You have 20 seconds to draw whatever image we give to you. After that we will test it to see if your drawing is good     enough for the AI model to match it to the image.</h1>"
, unsafe_allow_html=True)

how_to_img = "https://storage.googleapis.com/pictionary-ai-website-bucket/Screenshot%202024-03-14%20at%2012.42.34%20pm.png"
st.image(how_to_img, use_column_width=True)

add_vertical_space(3) #formatting

col1, col2, col3 = st.columns(3)

col1.write("")  # Empty column
col2.link_button(":yellow[Click here to play the game]", "https://pictionary-ai-frontend.streamlit.app/Game")  # Link button in the middle
col3.write("")  # Empty column

add_vertical_space(3) #formatting
st.markdown("<h1 style='text-align: center; font-weight: normal; font-size: 18px;'>Below are some examples of the sorts of images you may be asked to draw.</h1>", unsafe_allow_html=True)

image1 = 'https://storage.googleapis.com/pictionary-ai-website-bucket/preview.jpg'

st.image(image1, width=710) #bottom of page image
