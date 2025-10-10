**🧠 Resume Classifier**

**🎯 Objective**

A web-based tool for HR teams to upload resumes and job requirements, then compute a match score based on skills, experience, education, and salary. Parsed data is stored in MongoDB for future use.

**⚙️ Backend (FastAPI)**

Endpoint: /match_resume_job
Parsing: Extracts skills, education, experience, and salary using regex.
Matching: Uses TF-IDF + Cosine Similarity with skill weight boosting for better accuracy.
Storage: Parsed resume data saved in MongoDB.

**💻 Frontend (HTML + JS)**

Upload resume (PDF) and input job details (skills, experience, salary, education).
Displays:
Match score (%)
Skills matched
Parsed details
Responsive UI with error handling and loading indicator.

**🗄️ Database**

Each record in MongoDB includes:
File name
Parsed skills, education, experience, and salary

**🔁 Workflow**

HR uploads resume / enters job details.
Backend parses data → builds job text.
TF-IDF vectors + cosine similarity = match score.
Result displayed on frontend.
