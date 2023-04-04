import requests
import streamlit as st

# Set the FastAPI endpoint URL
endpoint_url = 'http://localhost:8000/convert'

# Create a Streamlit app
st.title("PDF to Text Converter")

# Add a file uploader to the app
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# If the user uploads a file, call the FastAPI endpoint to convert it
if uploaded_file is not None:

    # Send a POST request to the FastAPI endpoint with the PDF file attached
    response = requests.post(endpoint_url, files={"file": uploaded_file})

    # If the request was successful, display a link to the text file
    if response.status_code == 200:
        text_file_path = response.json()["text_file_path"]
        st.success(f"Conversion successful! Download the text file [here]({text_file_path}).")

    # If the request was not successful, display an error message
    else:
        st.error("Conversion failed. Please try again.")
