import pdfplumber
import re
import html
import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity


def keyword_match(text, keywords):
    return [kw for kw in keywords if kw.lower() in text.lower()]


def calculate_score(matched_keywords, total_keywords, text_length):
    keyword_score = (len(matched_keywords) / total_keywords) * 50
    length_score = min(text_length / 1000, 1) * 30
    return int(keyword_score + length_score + 20)


def extract_contact_info(text):
    email = re.findall(r"[\w\.-]+@[\w\.-]+", text)
    phone = re.findall(r"\b\d{10}\b", text)
    linkedin = re.findall(r"https://www.linkedin.com/in/\S+", text)
    address_match = re.search(r"Address[:\-]?\s*(.+?)(?=\n|Email|E-mail|Phone|LinkedIn|GitHub|$)", text, re.IGNORECASE)
    return {
        "Email": email[0] if email else "Not found",
        "Phone": phone[0] if phone else "Not found",
        "LinkedIn": linkedin[0] if linkedin else "Not found",
        "Address": address_match.group(1).strip() if address_match else "Not found"
    }


def match_job_description(resume_text, jd_text):
    jd_keywords = [word.strip().lower() for word in jd_text.split() if len(word) > 3]
    resume_keywords = resume_text.lower()
    matched = [kw for kw in jd_keywords if kw in resume_keywords]
    missing = list(set(jd_keywords) - set(matched))
    match_score = (len(matched) / len(jd_keywords)) * 100 if jd_keywords else 0
    return match_score, missing


def clean_line(line):
    line = line.strip().replace("•", "").replace("▪", "")
    line = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", line)  # Fixes merged words like "SeekinganEntry"
    if len(line) < 20 or line.isupper():
        return None
    if re.search(r"(club|event|sports|football|basketball|represented|council|hackathon)", line, re.IGNORECASE):
        return None
    if re.search(r"@|linkedin|www\.|Address|Phone|Email|KANISHKA SONI|India", line, re.IGNORECASE):
        return None
    return line


def generate_structured_summary(text):
    doc = nlp(text)
    lines = [clean_line(sent.text) for sent in doc.sents]
    lines = [line for line in lines if line]

    experiences = []
    projects = []
    education_skills = []

    for line in lines:
        lower = line.lower()

        if any(w in lower for w in ["intern", "experience", "team lead", "worked", "engineer", "role", "position"]):
            experiences.append(line)
        elif any(w in lower for w in ["project", "built", "developed", "implemented", "deployed", "dashboard", "summarizer"]):
            projects.append(line)
        elif any(w in lower for w in [
            "university", "degree", "certified", "education", "skills", "cloud", "language",
            "cgpa", "programming languages", "technologies", "tools", "competencies", "platforms"
        ]) or ":" in line:
            education_skills.append(line)

    parts = []
    if experiences:
        parts.append(f"{experiences[0]}")
    if projects:
        parts.append(f"Worked on projects like {projects[0]}")
    if education_skills:
        parts.append(f"Holds certifications or technical proficiencies such as: {education_skills[0]}")

    return "\n\n".join(parts[:3]).strip() if parts else "No meaningful summary generated."
