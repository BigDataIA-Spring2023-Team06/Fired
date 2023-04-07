import os
from fastapi import FastAPI, File, UploadFile
from pymongo import MongoClient
from PyPDF2 import PdfReader
import boto3
import botocore
import time
import io


app = FastAPI()

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

# s3_bucket = "goes-team6"

# Create the MongoClient using the SSL context object
client = MongoClient(mongo_uri, tlsAllowInvalidCertificates=True)

# Use the MongoClient instance to perform database operations
db = client[db_name]

#API to get the resume and job description from mongoDB
@app.get("/get_resume_and_job_description")
def get_resume_and_job_description(filename: str):
    collection_resume = db[collection_resume]
    collection_job_description = db[collection_job_description]
    document_resume = collection_resume.find_one({"_id": filename})
    document_job_description = collection_job_description.find_one({"_id": filename})
    return {"resume": document_resume, "job_description": document_job_description}


# #API endpoint to add job description to the mongoDB
@app.post("/add_job_description")
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

#API endpoint to upload file to S3 and the extracted text to mongoDB
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
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
        key = f"{file.filename}"
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

