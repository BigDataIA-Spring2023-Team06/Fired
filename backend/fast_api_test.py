from fastapi import FastAPI, File, UploadFile
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import gpt_helper

import PyPDF2

app = FastAPI()

@app.post("/convert")
async def convert(file: UploadFile = File(...)):

    # Open the uploaded PDF file in read-binary mode
    with open(file.filename, 'wb') as pdf_file:
        contents = await file.read()
        pdf_file.write(contents)

    # Create a PDF reader object
    with open(file.filename, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Create a text file for writing
        with open('output.txt', 'w') as txt_file:

            # Loop through all the pages in the PDF file
            for page_num in range(pdf_reader.getNumPages()):

                # Extract the text from the page
                page = pdf_reader.getPage(page_num)
                text = page.extractText()

                # Write the text to the text file
                txt_file.write(text)

    # Return the path to the text file
    return {"text_file_path": "output.txt"}


@app.get("/resume_question/")
async def get_resume_question(resume, no_of_questions):
    return {"resume_question" : gpt_helper.get_response_gpt(f"generate {no_of_questions} interview question from this resume {resume}")} 

@app.get("/jd_question/")
async def get_jd_question(job_description, no_of_questions):
    return {"question" : gpt_helper.get_response_gpt(f"generate {no_of_questions} interview question from this job description {job_description}")} 

@app.get("/resume_match/")
async def get_jd_question(resume, jd):
    return {"resume_feedback" : gpt_helper.get_response_gpt(f"tell if the candidate with this resume - {resume} is fit for role with the following job description - {jd} be honest and blunt")} 

# @app.get("/resume_match/")
# async def get_jd_question(resume, jd):
#     return {"resume_question" : gpt_helper.get_response_gpt(f"tell if the candidate with this resume - {resume} is fit for role with the following job description - {jd} be honest and blunt")} 

@app.get("/get_adjectives/")
async def get_adjectives(text):
    return {"adjectives" : gpt_helper.get_response_gpt(f"Generate 10 adjectives from this text without bullets - {text}")} 


####################Sentiment Analysis Api#########################

# model = 'cardiffnlp/twitter-xlm-roberta-base-sentiment'
@app.get("/sentiment/")
def sentiment_score(text: str):
    model_name = 'cardiffnlp/twitter-xlm-roberta-base-sentiment'
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    result = classifier(text)
    return {"result" : result} 

# text = '''
# Skeptical
# Doubtful
# Uncertain
# Apprehensive
# Ambiguous
# Inadequate
# Inconclusive
# Questionable
# Insufficient
# Indeterminate.
# '''
# print(sentiment_score(text))













