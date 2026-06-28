import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# -------- Extract text from PDF --------
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


# -------- Extract text from TXT --------
def extract_text_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read()


# -------- Main Ranking Function --------
def rank_multiple_resumes(resume_files, jd_file):
    resume_texts = []
    resume_names = []

    # Read resumes
    for file in resume_files:
        resume_texts.append(extract_text_from_pdf(file))
        resume_names.append(os.path.basename(file))

    # Read Job Description
    if jd_file.endswith(".pdf"):
        jd_text = extract_text_from_pdf(jd_file)
    elif jd_file.endswith(".txt"):
        jd_text = extract_text_from_txt(jd_file)
    else:
        raise ValueError("Unsupported Job Description format")

    documents = resume_texts + [jd_text]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    jd_vector = tfidf_matrix[-1]
    resume_vectors = tfidf_matrix[:-1]

    scores = cosine_similarity(resume_vectors, jd_vector)

    ranked_resumes = []
    for i, score in enumerate(scores):
        ranked_resumes.append((resume_names[i], round(score[0] * 10, 2)))

    ranked_resumes.sort(key=lambda x: x[1], reverse=True)
    return ranked_resumes
