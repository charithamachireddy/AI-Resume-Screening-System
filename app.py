from flask import Flask, render_template, request
import os
from resume_parser import extract_text_from_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Job required skills
job_skills = ["python", "sql", "machine learning", "html", "css", "javascript"]

@app.route("/", methods=["GET", "POST"])
def index():

    matched_skills = []
    score = 0

    if request.method == "POST":

        file = request.files["resume"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        resume_text = extract_text_from_pdf(filepath)
        resume_text = resume_text.lower()

        for skill in job_skills:
            if skill in resume_text:
                matched_skills.append(skill)

        # Calculate match percentage
        score = int((len(matched_skills) / len(job_skills)) * 100)

    return render_template("index.html", skills=matched_skills, score=score)

if __name__ == "__main__":
    app.run(debug=True)