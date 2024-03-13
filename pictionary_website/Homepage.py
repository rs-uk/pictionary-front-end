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

image1 = "https://ff6004531c4ed8d51bf2a0bdc2030173d63224bcf59aba4bb66a3cc-apidata.googleusercontent.com/download/storage/v1/b/pictionary-ai-website-bucket/o/pictionary_ai.jpg?jk=ATxpoHenezw7np-rnwNSpcBg9IA0mMWGlRyRy3Ll1GYCHnCfoDxpL1k84zu9gOls-rrfbB4UiiqDfdQRQRLUIK5zKQ8EmHpSDz570vREEqta0R2XH3G9-8x_DIq6R3fU1vy8-THh12_My0NwX6xKaN9T4qehIVFYJYXlPp1xY80I0hpuVx1QCB30kQoac-xNhQksoXKJ6bp9Uu0AtN9cjT99bdIH3E3TvnMzUn9JXUQNgszI3x-KU_-FWMi2IBWk89aHUU36R-17ymfVdA8cpON9ykkRIanH8ISucWqY0GwIqJ7-Kn2KlA7d96t2OExQXA-pGaf-27wngfXihr5UNIZxYemaX2wUocCC_u8RWmJcVl2o_WZEhUEAjRTODuSQQFE0X_uBZOxuQ3fadagLGGSZcZj2e4I7eKIkViiNsC3piJHdMi2tyF5_jQzGUXQtFQG1WWXi0JoJMXxVQFYBUclFyGMM2csAexEbANvX1LEORmlSBhdjuzjfjWdVUsZE9bGoO1w7-xA9NFT5GpD6Jq85ACJ7A2XAaQLFYVSpB0js24YZCQ9DachlQeXvi3fT8cMHtv8OLmHEGdJW5j62yN17xCuyTATNtg-fnRPIKGVz9QxfwfK4iRqQrxKejI0dtpk92HFgr3RGhiDvqzA3BojcEdJr2lqjkbMhcYUrl2Kvm_mUILCZ1O-vEexFPS5CJWn6KKn-pNkhjzegruNr-2wYD9uJAUklmiBnCsQbASsU21RyMsmHo8ku6uandKCRjVfyMGRJ4_R6aS_SULGlXUmY8IvEnNwioYINtMkKzgiWPCYlA9Wi8DHJH9dKzodLw1n60UaV1N9B8R2fd4Eyq1feRd2r4LnGQs-U8tFzUcSARavGQArfoerP6FQy2ENwlMibR3sI6OLSnhxHeH42S0x0IIoqSBYZRFNrS7wZjOiE8hhJ-DsKHS-MfUTTYhgMZfEsh3dBa7CGeNlYD4AHLaiiSFhf3Z6kv4nWKgZToYS9aYuwYiR1u2VmGm2W7qMUzjMBdi8eaGaHwyAKfBw5366moVVAOaRAy7THWFAl5Cg5wVqR-eca7327ihelWfVtXLwCRICucuWOA03NJlNtciw-IfQ1Kn0rulraE7_-oSzcSeWGTroAf9Kj5wbgszGSZTSuvKH9DLVswPGdDkykaHRfZNl89EPCjeNhm2CgtiWyjicUeV0uk5HGEpK7bJo&isca=1"
add_vertical_space(3) #formatting

col1, col2, col3 = st.columns(3)

col1.write("")  # Empty column
col2.link_button(":blue[Click here to play the game]", "http://localhost:8501/Game")  # Link button in the middle
col3.write("")  # Empty column

add_vertical_space(3) #formatting
st.markdown("<h1 style='text-align: center; font-weight: normal; font-size: 18px;'>Below are some examples of the sorts of images you may be asked to draw.</h1>", unsafe_allow_html=True)

image1 = 'https://storage.googleapis.com/pictionary-ai-website-bucket/preview.jpg'

st.image(image1, width=710) #bottom of page image
