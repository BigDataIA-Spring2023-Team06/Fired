import streamlit as st

import os

from PyPDF2 import PdfReader





st.title("FIRED!")

st.write("Upload your resume and enter a job description to get started")

# Add file uploader and dropdown for selecting resumes

uploaded_files = st.file_uploader("Upload one or more resumes", type="pdf", accept_multiple_files=True)

resume_names = [file.name for file in uploaded_files]

selected_resume = st.selectbox("Select a resume", resume_names)




# Add job description input

job_description = st.text_input("Job Description")




# Add three buttons

if st.button("Customized Resume Questions"):

    st.write("Customized Resume Questions")

if st.button("Role Based Questions"):

    st.write("Role Based Questions")

if st.button("Resume Match Details"):

    st.write("Resume Match Details")




# If a resume was selected

if selected_resume:

    # Read the contents of the selected resume

    for file in uploaded_files:

        if file.name == selected_resume:

            with open(file.name, 'rb') as f:

                pdf_reader = PdfReader(f)

                text = ""

                for page in pdf_reader.pages:

                    text += page.extract_text()




            # Display the selected resume

            st.write("Selected resume:")

            st.write(text)




# If a job description was entered

if job_description:

    # Display the entered job description

    st.write("Entered job description:")

    st.write(job_description)