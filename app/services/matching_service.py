from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text(text_list):
    """Join all fields (like skills, education, experience) into one string."""
    if not text_list:
        return ""
    if isinstance(text_list, list):
        return " ".join(text_list)
    return str(text_list)

def calculate_similarity(resume_data, job_data):
    """Compare resume and job post based on textual similarity (TF-IDF)."""
    
    # Combine key text fields
    resume_text = " ".join([
        preprocess_text(resume_data.get("parsed_skills")),
        preprocess_text(resume_data.get("parsed_education")),
        preprocess_text(resume_data.get("parsed_experience")),
    ])

    job_text = " ".join([
        preprocess_text(job_data.get("skills")),
        preprocess_text(job_data.get("education")),
        preprocess_text(job_data.get("experience")),
    ])

    # Vectorize both texts
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_text])

    # Compute cosine similarity
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    
    # Convert to percentage
    return round(similarity * 100, 2)
