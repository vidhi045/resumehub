# app/resume_parser.py
import pdfplumber
import re

# Define known skills
SKILLS = [
    "Python", "Java", "JavaScript", "SQL", "HTML", "CSS", "React", "Node.js",
    "AI", "Machine Learning", "Deep Learning", "Data Science", "MongoDB",
    "Django", "Flask", "C++", "C#", "AWS", "Docker"
]

# Education keywords (case-insensitive)
EDUCATION_KEYWORDS = ["B.Tech", "M.Tech", "Bachelor", "Master", "MBA", "PhD"]

# Regex patterns
EXPERIENCE_REGEX = re.compile(r"(\d+(\.\d+)?)\s*(years?|yrs?|months?|mos?)", re.I)
SALARY_REGEX = re.compile(r"(₹|\$)\s*\d+(,\d{3})*(\.\d+)?", re.I)

# ----------------- Extract text -----------------
def extract_text_from_pdf(file):
    """
    Extract text from a PDF file-like object
    """
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# ----------------- Extract skills -----------------
def extract_skills(text):
    found_skills = []
    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text, re.I):
            found_skills.append(skill)
    return found_skills

# ----------------- Extract education -----------------
def extract_education(text):
    found_edu = []
    for keyword in EDUCATION_KEYWORDS:
        matches = re.findall(keyword, text, re.I)
        found_edu.extend(matches)
    return list(set(found_edu))  # remove duplicates

# ----------------- Extract experience -----------------
def extract_experience(text):
    matches = EXPERIENCE_REGEX.findall(text)
    experience_list = []
    for match in matches:
        experience_list.append(match[0] + " " + match[2])  # e.g., "2 years"
    return experience_list

# ----------------- Extract salary expectations -----------------
def extract_salary_expectations(text):
    matches = SALARY_REGEX.findall(text)
    salary_list = []
    for match in matches:
        salary_list.append("".join(match))  # e.g., "₹5,00,000"
    return salary_list

# ----------------- Parse resume -----------------
def parse_resume(file):
    """
    Main function to parse uploaded resume file and return structured details
    """
    text = extract_text_from_pdf(file)
    parsed_data = {
        "parsed_skills": extract_skills(text),
        "parsed_education": extract_education(text),
        "parsed_experience": extract_experience(text),
        "parsed_salary": extract_salary_expectations(text)
    }
    return parsed_data
