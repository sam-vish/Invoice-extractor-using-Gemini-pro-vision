from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get responses

def get_gemini_response(inputs, images, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    responses = []
    for i in range(len(inputs)):
        response = model.generate_content([inputs[i], images[i], prompt])
        responses.append(response.text)
    return responses
    

def input_image_setup(uploaded_files):
    images = []
    # Check if files have been uploaded
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            # Read the file into bytes
            bytes_data = uploaded_file.getvalue()

            image_parts = {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
            images.append(image_parts)
        return images
    else:
        raise FileNotFoundError("No files uploaded")


##initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input_prompts = st.text_area("Input Prompts (Separate each prompt by a new line): ",key="input")
uploaded_files = st.file_uploader("Choose image(s)...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
images = []   
if uploaded_files is not None:
    images = [Image.open(file) for file in uploaded_files]
    for image in images:
        st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the images")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input images
               """

## If ask button is clicked

if submit:
    if not images:
        st.warning("Please upload at least one image.")
    else:
        input_prompts_list = input_prompts.split('\n')
        image_data = input_image_setup(uploaded_files)
        responses = get_gemini_response(input_prompts_list, image_data, input_prompt)
        for i, response in enumerate(responses):
            st.subheader(f"The Response for Image {i+1} is")
            st.write(response)
