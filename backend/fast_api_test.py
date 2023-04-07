from fastapi import FastAPI, File, UploadFile
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import gpt_helper
import boto3
import botocore
import os
import time
import io
from PyPDF2 import PdfReader
from pymongo import MongoClient
import PyPDF2

app = FastAPI()

#MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("MONGO_DB")
collection_resume = os.getenv("MONGO_COLLECTION_RESUMES")
collection_job_description = os.getenv("MONGO_COLLECTION_JD")

###################API to upload file to s3############################
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
s3_bucket = os.environ.get('S3_BUCKET')
region_name = os.environ.get('S3_REGION')

# Create a new S3 client
s3 = boto3.client('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Create the MongoClient using the SSL context object
client = MongoClient(mongo_uri, tlsAllowInvalidCertificates=True)

# Use the MongoClient instance to perform database operations
db = client[db_name]

# API to get the list of all resumes from MongoDB
@app.post("/get_resumes")
def get_resumes():
    collection = db[collection_resume]
    documents = collection.find()
    resumes = []
    for document in documents:
        resume_name = document["_id"]
        resumes.append(resume_name)
    return resumes

#API endpoint to upload file to S3 and the extracted text to mongoDB
@app.post("/uploadfile/")
async def upload_file(filename:str ,file: UploadFile = File(...)):
    """
    Uploads a file to an S3 bucket.
    """
    try:
        text = ""
        content = await file.read()  # Read the content of the file
        pdf_reader = PdfReader(io.BytesIO(content))
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Generate a unique key for the file
        key = f"{int(time.time())}-{filename}"
        # Add resume to mongoDB
        document = {"_id": key, "resume": text}
        collection = db[collection_resume]
        result = collection.insert_one(document)
        # Upload the file to S3
        s3.upload_fileobj(io.BytesIO(content), s3_bucket, f"resumes/{key}")
        
        return {"message": "File uploaded successfully!", "filename_in_s3":key, "mongo_inserted_id": str(result.inserted_id)}
    except botocore.exceptions.ParamValidationError as e:
        return {"error": f"Parameter validation error: {e}"}
    except botocore.exceptions.ClientError as e:
        return {"error": f"Client error: {e}"}

#API to get the resume and job description from mongoDB
@app.get("/get_resume_and_job_description/")
def get_resume_and_job_description(filename: str):
    col_resume = db[collection_resume]
    col_job_description = db[collection_job_description]
    document_resume = col_resume.find_one({"_id": filename})
    document_job_description = col_job_description.find_one({"_id": filename})
    return {"resume": document_resume, "job_description": document_job_description}

#API to empty out the resume and job description collection
@app.get("/empty_resume_and_job_description/")
def empty_resume_and_job_description():
    col_resume = db[collection_resume]
    col_job_description = db[collection_job_description]
    col_resume.delete_many({})
    col_job_description.delete_many({})
    return {"message": "Resume and Job Description collections are empty now"}

# #API endpoint to add job description to the mongoDB
@app.get("/add_job_description/")
def add_job_description(filename:str, job_description: str):
    collection = db[collection_job_description]
    document = {"_id": filename, "job_description": job_description}
    result = collection.insert_one(document)
    return {"message": "Job Description added successfully!", "mongo_inserted_id": str(result.inserted_id)}

#API Endpoint to get the resume from mongoDB
@app.get("/get_resume")
def get_resume(filename: str):
    collection = db[collection_resume]
    document = collection.find_one({"_id": filename})
    return document

@app.get("/resume_question/")
async def get_resume_question(resume, no_of_questions):
    return {"resume_question" : gpt_helper.get_response_gpt(f"generate {no_of_questions} interview question from this resume {resume}")} 

@app.get("/jd_question/")
async def get_jd_question(job_description, no_of_questions):
    return {"question" : gpt_helper.get_response_gpt(f"generate {no_of_questions} interview question from this job description {job_description}")} 

@app.get("/resume_match/")
async def get_jd_question(resume, jd):
    return {"resume_feedback" : gpt_helper.get_response_gpt(f"evaluate and provide insights to the best of your abilities if the candidate with the follwing resume: {resume} is fit for role with the following job description - {jd}")} 

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













