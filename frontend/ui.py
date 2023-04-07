import streamlit as st
import os
from PyPDF2 import PdfReader
import requests 


host = 'http://localhost:8000'
headers = {'accept': 'application/json'}
ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

st.set_page_config(page_title="FIRED!", page_icon=":guardsman:")

# Add CSS to set the background image
st.markdown(
    """
    <style>
    body {
        background-image: url('https://www.pexels.com/photo/black-sand-dunes-2387793/');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("FIRED!")
st.write("Upload your resume and enter a job description to get started")
# Add file uploader and dropdown for selecting resumes
file = st.file_uploader("Upload one or more resumes", type="pdf", accept_multiple_files=False)

if file is not None:
    if True:
        files = {"file": file.getvalue()}
        # Call the API
        response = requests.post(f"{host}/uploadfile/", headers=headers, files=files)
        
        if response.status_code == 200:
            st.success("File uploaded successfully")
            st.write(response.json()["filename_in_s3"])
                
                
resume_names = ["ABC", "DEF"]
selected_resume = st.selectbox("Select a resume", resume_names)

# Add job description input
job_description = st.text_input("Job Description")
resume = st.text_input("Paste Your Resume Here")

# Add three buttons
if st.button("Customized Resume Questions"):
    st.write("Customized Resume Questions")
    
if st.button("Role Based Questions"):
    st.write("Role Based Questions")
    params = {"job_description": job_description, "no_of_questions": 1}
    response = requests.get(f"{host}/jd_question/", params=params)
    if response.status_code == 200:
        st.write(response.json()["question"])

if st.button("Resume Match Details"):
    st.write("Resume Match Details")
    
    params = {"resume": resume, "jd": job_description}
    response = requests.get(f"{host}/resume_match/", params=params)
    if response.status_code == 200:
        feedback = response.json()["resume_feedback"]
        st.write(feedback)
        
        params = {"text":feedback}
        response_adjectives = requests.get(f"{host}/get_adjectives/", params=params)
        if response_adjectives.status_code == 200:
            adjectives = response_adjectives.json()['adjectives']
            params_adjective = {"text":adjectives}
            print(adjectives)
            match = requests.get(f"{host}/sentiment/", params = params_adjective)
            st.write("Processing")
            
            if match.status_code == 200:
                match_perc = match.json()
                st.write(match_perc)
                print(match_perc)
            else:
                st.write("Failed to Load Sentiment Analysis Model")
            
         
         

# If a resume was selected
# if selected_resume:
#     # Read the contents of the selected resume
#     for file in uploaded_files:
#         if file.name == selected_resume:
#             with open(file.name, 'rb') as f:
#                 pdf_reader = PdfReader(f)
#                 text = ""
#                 for page in pdf_reader.pages:
#                     text += page.extract_text()

            # # Display the selected resume
            # st.write("Selected resume:")
            # st.write(text)

# If a job description was entered
# if job_description:
    # Display the entered job description
    # st.write("Entered job description:")
    # st.write(job_description)
