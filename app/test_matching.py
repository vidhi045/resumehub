from app.services.matching_service import calculate_similarity

resume_data = {
    "parsed_skills": ["Python", "SQL", "HTML", "CSS", "JavaScript"],
    "parsed_education": ["B.Tech"],
    "parsed_experience": ["2 years"]
}

job_data = {
    "skills": ["Python", "Django", "SQL", "React"],
    "education": ["B.Tech"],
    "experience": "2 years"
}

score = calculate_similarity(resume_data, job_data)
print(f"🔍 Resume–Job Match Score: {score}%")
