from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")  # adjust URI
db = client["resume_db"]
resumes_collection = db["resumes"]
