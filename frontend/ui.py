import streamlit as st
import requests 
import json

# Set default layout to wide mode
st.set_page_config(
    page_title="Fired!",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the session state
class SessionState:
    def __init__(self):
        self.file = None

# Create an instance of the session state
state = SessionState()

# Define a function to clear the file from session state
def clear_file():
    state.file = None

host = 'http://localhost:8000'
headers = {'accept': 'application/json'}
ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
col1, col2,col3= st.columns(3)





with col1:
    def file_upload():
        st.header("Upload Resume")
    # st.write("Upload your resume and enter a job description to get started")
    # Add file uploader and dropdown for selecting resumes
        file = st.file_uploader("Upload one or more resumes", type="pdf", accept_multiple_files=False)
        # Optional name for the file
        default_name = "_"
        filename_ext = st.text_input("Optional Filename",default_name)
        submit_resume = st.button("Submit Resume")
        if submit_resume:
            if file is not None:
                params={"filename": f"{filename_ext}{file.name}"}
                files = {"file": file.getvalue()}
                # Call the API to upload the file to S3 and add the resume to MongoDB
                response = requests.post(f"{host}/uploadfile/", headers=headers, files=files, params=params)
                if response.status_code == 200:
                    st.success("File uploaded successfully")
                    st.write(f"""File Name for reference: {response.json()["filename_in_s3"]}""")
                    file = None
                else:
                    st.error("File upload failed")
        file = None

    file_upload()
submit_jd = False
selected_resume = "Select a resume"
with col2:
    st.header("Pick Resume and Add Job Description")
    response_names = requests.post(f"{host}/get_resumes")
    names= response_names.json()
    names.insert(0, "Select a resume")
    selected_resume = st.selectbox("Select a resume", names)
    if selected_resume != "Select a resume":
        jd = st.text_input("Job Description")
        submit_jd = st.button("Submit")
        if submit_jd:
            params = {"filename": selected_resume, "job_description": jd}
            response = requests.get(f"{host}/add_job_description/", params=params)
            if response.status_code == 200:
                st.write(response.json()["message"])
            else:
                st.error("Job description not added")

        # params = {"resume_name": selected_resume}
        # response = requests.post(f"{host}/add_resume/", params=params)
        # if response.status_code == 200:
        #     st.success("Resume added successfully")


    # if job_description is not None:
    #     #Add job description to mongodb
 






    
# # resume_names = 
# # selected_resume = st.selectbox("Select a resume", resume_names)

# # # Add job description input
# # job_description = st.text_input("Job Description")
# # resume = st.text_input("Paste Your Resume Here")
with col3:
    st.header("Analytics")
    # Get resume and job description from mongodb
    params_rs_jd = {"filename": selected_resume}
    response = requests.get(f"{host}/get_resume_and_job_description/", params=params_rs_jd)
    job_description_new = response.json()["job_description"]
    resume_new = response.json()["resume"]
    params_jd_qs = {"job_description": job_description_new, "no_of_questions": 1}
    response = requests.get(f"{host}/jd_question/", params=params_jd_qs)
    if response.status_code == 200:
        st.write("Role Based Questions")
        st.write(response.json()["question"])
    if job_description_new is not None:
        params_match = {"resume": resume_new, "jd": job_description_new}
        response = requests.get(f"{host}/resume_match/", params=params_match)
        if response.status_code == 200:
            feedback = response.json()["resume_feedback"]
            st.write(feedback)
        params_resume_qs = {"resume": resume_new, "no_of_questions": 1}
        response = requests.get(f"{host}/resume_question/", params=params_resume_qs)
        if response.status_code == 200:
            st.write("Customized Resume Questions")
            st.write(response.json()["resume_question"])
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


#     # Add three buttons
#     if st.button("Customized Resume Questions"):
#         st.write("Customized Resume Questions")
        
#     if st.button("Role Based Questions"):
#         st.write("Role Based Questions")
#         params = {"job_description": job_description, "no_of_questions": 1}
#         response = requests.get(f"{host}/jd_question/", params=params)
#         if response.status_code == 200:
#             st.write(response.json()["question"])

#     if st.button("Resume Match Details"):
#         st.write("Resume Match Details")
        
#         params = {"resume": selected_resume, "jd": job_description}
#         response = requests.get(f"{host}/resume_match/", params=params)
#         if response.status_code == 200:
#             feedback = response.json()["resume_feedback"]
#             st.write(feedback)
            
#             params = {"text":feedback}
#             response_adjectives = requests.get(f"{host}/get_adjectives/", params=params)
#             if response_adjectives.status_code == 200:
#                 adjectives = response_adjectives.json()['adjectives']
#                 params_adjective = {"text":adjectives}
#                 print(adjectives)
#                 match = requests.get(f"{host}/sentiment/", params = params_adjective)
#                 st.write("Processing")
                
#                 if match.status_code == 200:
#                     match_perc = match.json()
#                     st.write(match_perc)
#                     print(match_perc)
#                 else:
#                     st.write("Failed to Load Sentiment Analysis Model")
                
            
         

# # If a resume was selected
# # if selected_resume:
# #     # Read the contents of the selected resume
# #     for file in uploaded_files:
# #         if file.name == selected_resume:
# #             with open(file.name, 'rb') as f:
# #                 pdf_reader = PdfReader(f)
# #                 text = ""
# #                 for page in pdf_reader.pages:
# #                     text += page.extract_text()

#             # # Display the selected resume
#             # st.write("Selected resume:")
#             # st.write(text)

# # If a job description was entered
# # if job_description:
#     # Display the entered job description
#     # st.write("Entered job description:")
#     # st.write(job_description)
