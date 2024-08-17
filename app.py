# Q&A Chatbot

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure API key for the generative AI client
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Initialize our Streamlit app with improved UI
st.set_page_config(page_title="Gemini Invoice Analyzer", page_icon=":page_facing_up:", layout="centered")

# Main container for the application
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Gemini Invoice Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload an image of an invoice and get insights.</p>", unsafe_allow_html=True)

# Input prompt and file uploader with column layout for a more polished look
input_col, upload_col = st.columns(2)

with input_col:
    input = st.text_input("Describe the Image:", key="input", placeholder="e.g., Tell me about this invoice")

with upload_col:
    uploaded_file = st.file_uploader("Upload Invoice Image:", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True, channels="RGB")

# Center the button and response area
submit_col, _ = st.columns([1, 3])

with submit_col:
    submit = st.button("Analyze Invoice", type="primary")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

# Response section
if submit:
    if uploaded_file:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input)
        st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Response</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='padding: 10px; background-color: #333; color: white; border-radius: 5px;'>{response}</p>", unsafe_allow_html=True)
    else:
        st.error("Please upload an image.")
