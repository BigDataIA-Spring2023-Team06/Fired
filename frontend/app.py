import requests
host = 'http://localhost:8000'
# import streamlit as st

# # Set the FastAPI endpoint URL
# endpoint_url = 'http://localhost:8000/convert'

# # Create a Streamlit app
# st.title("PDF to Text Converter")

# # Add a file uploader to the app
# uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# # If the user uploads a file, call the FastAPI endpoint to convert it
# if uploaded_file is not None:

#     # Send a POST request to the FastAPI endpoint with the PDF file attached
#     response = requests.post(endpoint_url, files={"file": uploaded_file})

#     # If the request was successful, display a link to the text file
#     if response.status_code == 200:
#         text_file_path = response.json()["text_file_path"]
#         st.success(f"Conversion successful! Download the text file [here]({text_file_path}).")

#     # If the request was not successful, display an error message
#     else:
#         st.error("Conversion failed. Please try again.")



jd = '''LHH Recruitment Solutions is seeking a Staff Accountant for our Broomfield area client. The ideal candidate will have some experience in general ledger accounting and accounts payable and receivable transactions. This is a great opportunity for an individual seeking to take the next step and grow in their career.


Primary responsibilities of the Staff Accountant include:

Full cycle general ledger accounting, including account reconciliations
Preparation of daily journal entries
Reconciliation of general ledger and bank accounts
Correspondence with vendors and customers regarding accounts
Review and analysis of transactions and account activity
Preparation and review of monthly financial statements

Requirements:

Bachelor’s degree in accounting or finance
1+ year of general ledger accounting experience
Sound understanding and practical application of GAAP
Effective communication skills, both written and verbal
ERP accounting software experience'''

params = {"job_description": jd, "no_of_questions": 1}
print(requests.get(f"{host}/jd_question/", params=params).json()["question"])
