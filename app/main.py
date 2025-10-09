# app/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from app.services.resume_parser import parse_resume
from app.services.job_parser import parse_job_post
from app.database import resumes_collection
import pdfplumber

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- PDF text extraction ----------------
def extract_text_from_upload(file):
    text = ""
    file.seek(0)
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# ---------------- Build job text ----------------
def build_job_text(job_data):
    skills = " ".join(job_data.get("skills", []))
    experience = str(job_data.get("experience") or "")
    education = " ".join(job_data.get("education") or [])
    salary = str(job_data.get("salary") or "")
    job_text = f"{skills} {experience} {education} {salary}"
    return job_text

# ---------------- Skills matched ----------------
def get_skills_matched(resume_skills, job_skills):
    return [skill for skill in job_skills if skill in resume_skills]

# ---------------- Boost TF-IDF skill weights ----------------
def boost_skill_weights(vectorizer: TfidfVectorizer, vectors: csr_matrix, skills: list, factor: float = 5.0):
    feature_names = vectorizer.get_feature_names_out()
    indices_to_boost = [i for i, f in enumerate(feature_names) if f.lower() in [s.lower() for s in skills]]
    if indices_to_boost:
        vectors = vectors.tocsc(copy=True)
        for idx in indices_to_boost:
            vectors[:, idx] = vectors[:, idx] * factor
        vectors = vectors.tocsr()
    return vectors

# ---------------- Endpoint ----------------
@app.post("/match_resume_job")
async def match_resume_job(
    resume: UploadFile = File(...),
    skills: str = Form(...),
    experience: str = Form(""),
    education: str = Form(""),
    salary: str = Form("")
):
    # 1️⃣ Parse resume and get structured data
    parsed_resume = parse_resume(resume.file)

    # 2️⃣ Extract full text from PDF for TF-IDF
    resume_text = extract_text_from_upload(resume.file)

    # 3️⃣ Parse manual job inputs
    job_data = parse_job_post(skills=skills, experience=experience, salary=salary, education=education)
    job_text = build_job_text(job_data)

    # 4️⃣ Compute TF-IDF similarity
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_text])
    vectors = boost_skill_weights(vectorizer, vectors, skills=job_data.get("skills", []), factor=5.0)
    score = cosine_similarity(vectors[0], vectors[1])[0][0]

    # 5️⃣ Identify skills matched
    skills_matched = get_skills_matched(parsed_resume["parsed_skills"], job_data.get("skills", []))

    # 6️⃣ Store resume in MongoDB
    resume.file.seek(0)
    resume_bytes = resume.file.read()
    resume_doc = {
        "filename": resume.filename,
        "parsed_skills": parsed_resume["parsed_skills"],
        "parsed_education": parsed_resume["parsed_education"],
        "parsed_experience": parsed_resume["parsed_experience"],
        "parsed_salary": parsed_resume["parsed_salary"],
        "job_inputs": job_data,
        "file_data": resume_bytes
    }
    resumes_collection.insert_one(resume_doc)

    # 7️⃣ Return results
    return {
        "match_score": round(score * 100, 2),
        "skills_matched": skills_matched,
        "parsed_skills": parsed_resume["parsed_skills"],
        "parsed_education": parsed_resume["parsed_education"],
        "message": "Resume stored in database successfully"
    }
