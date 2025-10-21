# app/resume_parser.py
import pdfplumber
import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

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

# ----------------- Extract skills from Required Skills section -----------------
def extract_skills(text):
    """
    Extract only technical skills from the 'Required Skills' section using spaCy.
    Stops before the next section heading.
    Handles variations like 'Required Skills:', 'Required Skills & Tools:', 'Requirements:'
    """
    # 1️⃣ Extract Required Skills section (handles different headers)
    skills_section_pattern = r"(Required Skills(?: & Tools)?|Requirements)\s*[:\-]?\s*(.*?)(?=\n[A-Z][A-Za-z\s&]*\n|\Z)"
    match = re.search(skills_section_pattern, text, re.S | re.I)
    skills_section = match.group(2) if match else text

    doc = nlp(skills_section)
    skills = set()

    # 2️⃣ Named Entities (tools, libraries, frameworks)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "LANGUAGE", "WORK_OF_ART"]:
            skills.add(ent.text.strip())

    # 3️⃣ Noun chunks (multi-word skills)
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.strip()
        if len(chunk_text) > 1 and chunk_text.lower() not in {
            "understanding", "knowledge", "skills", "problem-solving", "foundation",
            "experience", "familiarity", "good", "basic"
        }:
            skills.add(chunk_text)

    # 4️⃣ Phrases inside parentheses (Regression, Classification, etc.)
    for match in re.findall(r'\((.*?)\)', skills_section):
        for term in match.split(','):
            term = term.strip()
            if len(term) > 1:
                skills.add(term)

    # 5️⃣ Slash-separated terms (TensorFlow / Keras / PyTorch)
    for match in re.findall(r'\b([A-Za-z\-]+(?: / [A-Za-z\-.]+)+)\b', skills_section):
        for term in match.split('/'):
            term = term.strip()
            if len(term) > 1:
                skills.add(term)

    # 6️⃣ Return sorted list
    return sorted(skills)

# ----------------- Extract education -----------------
def extract_education(text):
    """
    Dynamically detect education-related qualifications and institutions
    """
    degree_pattern = r"(B\.?Tech|M\.?Tech|Bachelor|Master|MBA|Ph\.?D)"
    institute_pattern = r"(University|College|Institute|School of [A-Za-z]+)"

    degrees = re.findall(degree_pattern, text, re.I)
    institutes = re.findall(institute_pattern, text, re.I)

    return {
        "degrees": list(set(degrees)),
        "institutes": list(set(institutes))
    }

# ----------------- Extract experience -----------------
def extract_experience(text):
    """
    Extract years/months of experience
    """
    matches = EXPERIENCE_REGEX.findall(text)
    experience_list = [match[0] + " " + match[2] for match in matches]
    return experience_list

# ----------------- Extract salary expectations -----------------
def extract_salary_expectations(text):
    """
    Extract salary figures
    """
    matches = SALARY_REGEX.findall(text)
    salary_list = ["".join(match) for match in matches]
    return salary_list

# ----------------- Parse job post -----------------
def parse_job_post(skills, experience, salary, education):
    # Dynamically clean and extract data
    job_skills = [s.strip() for s in skills.split(",") if s.strip()]
    job_education = re.findall(r"(B\.?Tech|M\.?Tech|Bachelor|Master|MBA|PhD)", education, flags=re.I)

    return {
        "skills": job_skills,
        "experience": experience.strip(),
        "education": job_education,
        "salary": salary.strip(),
    }

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
