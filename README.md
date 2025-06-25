# 📄 Smart Resume Analyzer

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-orange.svg)](https://streamlit.io/)

Smart Resume Analyzer is an AI-powered tool that helps you analyze, summarize, and compare resumes. Built using **Python**, **Streamlit**, **spaCy**, and **pdfplumber**, it provides structured insights, clean summaries, keyword matching, and job-fit scoring — all through a user-friendly web interface.

---

## 🚀 Features

- 📂 **Compare Two Resumes Side-by-Side**
  - AI-generated concise summaries
  - Resume score (out of 100) based on keyword match and structure
  - Sentiment analysis for language tone
  - Exportable comparison as CSV

- 📄 **Analyze a Single Resume**
  - Extract contact details (email, phone, LinkedIn)
  - Generate structured 2–3 paragraph summaries (no raw bullet dumps)
  - Get resume score and matched keywords
  - View sentiment polarity and subjectivity

- 🧠 **Match Resume to Job Description**
  - Paste a job description and match it against an uploaded resume
  - Identify missing keywords
  - Get match score in %

---

## 📸 Screenshots

![image](https://github.com/user-attachments/assets/419a69cd-3687-4b23-bbd0-a43418ba83e5)
![image](https://github.com/user-attachments/assets/82f66ebd-29af-488f-9512-5d31be4ccb13)
![image](https://github.com/user-attachments/assets/80cff2ba-ddf4-47ad-addf-92df4e333e82)
![image](https://github.com/user-attachments/assets/af2940df-f723-4fd4-9889-f58bf9424e44)

> 📄 Resume Summaries  
> ![Resume Summary](screenshots/resume_summary.png)

> 📊 Resume Comparison  
> ![Resume Comparison](screenshots/resume_comparison.png)

---

## 🧠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Text Processing**: [spaCy](https://spacy.io/), [TextBlob](https://textblob.readthedocs.io/)
- **PDF Parsing**: [pdfplumber](https://github.com/jsvine/pdfplumber)
- **Language**: Python 3.10+

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-resume-analyzer.git
cd smart-resume-analyzer
````

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
# Activate:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Run the App

```bash
streamlit run app.py
```

Visit `http://localhost:8501` to open the web interface.

---

## 📁 Project Structure

```
smart-resume-analyzer/
├── app.py                # Main Streamlit interface
├── utils.py              # Resume parsing, scoring, summarizing
├── requirements.txt      # Required dependencies
├── README.md             # Project documentation
└── screenshots/          # Demo screenshots (optional)
```

---

## 💡 To-Do / Upcoming Features

* [ ] PDF/Word export of summaries
* [ ] Resume ranking mode (multi-upload)
* [ ] Summary style toggle (short vs full)
* [ ] Dark theme support

---
## 🙌 Acknowledgements

* [Streamlit](https://streamlit.io/)
* [spaCy](https://spacy.io/)
* [pdfplumber](https://github.com/jsvine/pdfplumber)
* [TextBlob](https://textblob.readthedocs.io/)

