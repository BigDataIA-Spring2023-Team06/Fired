import openai
import boto3 


openai.api_key = ""

def get_response_gpt(query):
    
    
    response =  openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", 
        messages = [
            {"role" : "user", "content" : query }
        ]
    )
    return response["choices"][0]["message"]["content"]


# jd = '''LHH Recruitment Solutions is seeking a Staff Accountant for our Broomfield area client. The ideal candidate will have some experience in general ledger accounting and accounts payable and receivable transactions. This is a great opportunity for an individual seeking to take the next step and grow in their career.


# Primary responsibilities of the Staff Accountant include:

# Full cycle general ledger accounting, including account reconciliations
# Preparation of daily journal entries
# Reconciliation of general ledger and bank accounts
# Correspondence with vendors and customers regarding accounts
# Review and analysis of transactions and account activity
# Preparation and review of monthly financial statements

# Requirements:

# Bachelor’s degree in accounting or finance
# 1+ year of general ledger accounting experience
# Sound understanding and practical application of GAAP
# Effective communication skills, both written and verbal
# ERP accounting software experience'''

# resume = '''Master of Science, Information Systems (Big Data Systems and Analytics) GPA: 3.7/4 May 2024 Northeastern University, Boston
# Data Science Engineering and Tools, Advances in Data Science and Architecture, Big Data Systems and Intelligent Analytics Bachelor of Technology, Electronics and Communication Engineering June 2020 Manipal University Jaipur, Jaipur
# Data Structures and Algorithms in C++, Introduction to Data Science, Programming in Python
# Skills
# • Programming Languages: Python, SQL, R, Java, JavaScript
# • AWS Services: Lambda, S3, ECS, RDS, EC2, ALB, CloudWatch, Redshift, DynamoDB, Data Pipeline
# • Database: Data Warehouse (Snowflake, Big Query, Hive), Relational Database (MySQL, MS SQL Server, Postgres)
# • Python Libraries: Scikit-learn, PyTorch, NumPy, Pandas, Matplotlib, Streamlit, FastAPI, unittest, boto3
# • Platforms/Tools: Tableau, Terraform, Airflow, Docker, Linux, Hadoop, Git, Excel, Azure
# Professional Experience Data Engineer (Senior Software Engineer) Dec 2021 - July 2022 Capgemini, Navi Mumbai, Maharashtra
# • Spearheaded the development of reconciliation framework in a fast-paced agile environment for CSV and JSON datasets, developed stored procedures using SQL for automated error handling in real time, reducing operational costs by 60%
# • Collaborated with a team of data engineers and cloud architects to implement a serverless architecture for streaming data pipelines using Snowflake as data warehouse, AWS Lambda, S3 and SNS for ingestion of 2,000,000 rows of data
# • Led database schema designing and implementation of ETL pipelines for data transformation of 15 semi-structured data sets resulting in a well-structured relational data model improving data analysis efficiency by 70%
# • Leveraged AWS Lambda functions scripted in Python to validate the quality of CSV and JSON data files stored in S3 buckets and configured Amazon SNS to send notifications, resulting in 45% increase in data quality
# Cloud Engineer (Software Engineer) Oct 2020 - Nov 2021
# Capgemini, Navi Mumbai, Maharashtra
# • Created scalable AWS cloud infrastructure-as-code leveraging Terraform Cloud and Docker for handling high volume of insurance quote requests with EC2, RDS, Lambda, S3 buckets, ALB resulting in an 85% reduction in infrastructure cost
# • Optimized development process through the implementation of CI/CD pipelines and automation of Terraform code generation using AWS Lambda, Python scripting, DynamoDB and GitHub API resulting in a 75% decrease in overall cost
# Business Intelligence Intern Jan 2020 - April 2020
# Capgemini, Pune, Maharashtra
# • Conducted comprehensive data exploration and statistical analysis on massive datasets using Spark and Hive on AWS, uncovering actionable insights and valuable statistics
# • Leveraged Tableau to create an interactive dashboard that effectively visualized and communicated the insights to stakeholders, driving impactful decision-making and improving overall business reporting
# Projects Data Exploration tool for Radar and Satellite Data Dec 2022 - Feb 2023
# • Developed and deployed a Data as a Service web application with Streamlit as the front end and FastAPI as back-end, providing users with access to over 500 terabytes of NexRad and GOES satellite data
# • Implemented Airflow for orchestration along with AWS technologies including S3, RDS, CloudWatch, and Glue to process, store and extract data efficiently, leading to a 50% improvement in data processing performance
# • Utilized Altair and CloudWatch logs to design a BI dashboard, effectively visualizing and reporting on key user activity metrics for optimized decision-making
# Heroic Word Analysis & Movie Genre Prediction with Machine Learning Aug 2022 - Oct 2022
# • Extracted 500 movie scripts using Beautiful Soup from imdsb.com, cleaned and loaded the dialogues along with genre into a Pandas data frame and trained an SVC model to predict the genre of the movie with 92% accuracy
# • Developed a Bayesian simulation-based negative binomial model to analyze the presence of heroic words in the Lord of the Rings trilogy based on statistics derived from frequency of dialogue spoken by characters aligned with good and evil'''



# # print(get_response_gpt(f"can you tell if the candidate with this resume - {resume} is fit for role with the following job description - {jd} be honest and blunt"))

