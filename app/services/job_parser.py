import re
from app.services.resume_parser import SKILLS, EDUCATION_KEYWORDS

EXPERIENCE_REGEX = re.compile(r"(\d+(\.\d+)?)\s*(years?|yrs?|months?|mos?)", re.I)
SALARY_REGEX = re.compile(r"(₹|\$)\s*\d+(,\d{3})*(\.\d+)?", re.I)
EDUCATION_REGEX = re.compile(r"\b(" + "|".join(EDUCATION_KEYWORDS) + r")\b", re.I)

def extract_job_skills(skills_input: str):
    """Split comma-separated skills and validate against known SKILLS list."""
    skills = [s.strip() for s in skills_input.split(",") if s.strip()]
    validated = [s for s in skills if any(re.fullmatch(skill, s, re.I) for skill in SKILLS)]
    return validated

def extract_job_experience(exp_input: str):
    match = EXPERIENCE_REGEX.findall(exp_input)
    return match[0][0] + " " + match[0][2] if match else None

def extract_job_salary(salary_input: str):
    match = SALARY_REGEX.findall(salary_input)
    return "".join(match[0]) if match else None

def extract_job_education(education_input: str):
    matches = EDUCATION_REGEX.findall(education_input)
    return list(set(matches)) if matches else None

def parse_job_post(skills="", experience="", salary="", education=""):
    """Return parsed job post details as a dict from form inputs."""
    return {
        "skills": extract_job_skills(skills),
        "experience": extract_job_experience(experience),
        "salary": extract_job_salary(salary),
        "education": extract_job_education(education)
    }
