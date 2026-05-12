
from flask import Flask, render_template, request
import PyPDF2
import re

app = Flask(__name__)

skills_list = [
    "python", "java", "html", "css", "javascript",
    "sql", "react", "node", "flask", "django",
    "machine", "learning", "data", "analysis"
]
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['resume']
    job_desc = request.form['job_desc']

    if file:
        pdf_reader = PyPDF2.PdfReader(file)
        resume_text = ""

        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        # convert to lowercase
        resume_text = resume_text.lower()
        job_desc = job_desc.lower()

        # extract words
        resume_words = set(re.findall(r'\w+', resume_text))
        job_words = set(re.findall(r'\w+', job_desc))
        
        skills_list = ["python", "html", "css", "javascript", "sql", "java", "flask"]

        matched_words = resume_words.intersection(job_words).intersection(skills_list)
        missing_words = set(skills_list).intersection(job_words) - resume_words
        

        # score calculation
        score = (len(matched_words) / len(set(skills_list).intersection(job_words))) * 100 if job_words else 0

    

        return render_template(
         'result.html',
          score=round(score, 2),
         matched=matched_words,
          missing=missing_words
)

    else:
        return "No file uploaded"
# all your routes above...

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


    
