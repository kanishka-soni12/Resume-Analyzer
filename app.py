import streamlit as st
import os
import pandas as pd
from utils import (
    extract_text_from_pdf,
    analyze_sentiment,
    keyword_match,
    calculate_score,
    extract_contact_info,
    generate_structured_summary,
    match_job_description
)

st.set_page_config(page_title="Smart Resume Analyzer", layout="wide", page_icon="📄")
st.title("📄 Smart Resume Analyzer")

tab1, tab2, tab3 = st.tabs(["🆚 Compare Resumes", "📈 Individual Analysis", "🔍 JD Match"])

# Compare Two Resumes
with tab1:
    st.subheader("Upload and Compare Two Resumes")
    col1, col2 = st.columns(2)
    with col1:
        resume1 = st.file_uploader("Upload Resume 1", type="pdf", key="r1")
    with col2:
        resume2 = st.file_uploader("Upload Resume 2", type="pdf", key="r2")

    if resume1 and resume2:
        for i, res in enumerate([resume1, resume2], start=1):
            with open(f"temp_resume{i}.pdf", "wb") as f:
                f.write(res.read())

        text1 = extract_text_from_pdf("temp_resume1.pdf")
        text2 = extract_text_from_pdf("temp_resume2.pdf")

        keywords = ["python", "machine learning", "data science", "azure", "sql", "react", "cloud", "tensorflow"]

        result_data = []
        for idx, text in enumerate([text1, text2], start=1):
            polarity, _ = analyze_sentiment(text)
            matched = keyword_match(text, keywords)
            score = calculate_score(matched, len(keywords), len(text))
            result_data.append({
                "Resume": f"Resume {idx}",
                "Score (/100)": score,
                "Sentiment": round(polarity, 2),
                "Matched Keywords": ", ".join(matched) if matched else "None"
            })

        df = pd.DataFrame(result_data)
        st.markdown("### 📊 Comparison Table")
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="comparison.csv", mime="text/csv")

        st.markdown("### 🧠 Auto-Generated Summaries")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📄 Resume 1 Summary")
            st.markdown(f"<div style='background:#f9f9f9;padding:10px;border-radius:10px;'>{generate_structured_summary(text1)}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("#### 📄 Resume 2 Summary")
            st.markdown(f"<div style='background:#f9f9f9;padding:10px;border-radius:10px;'>{generate_structured_summary(text2)}</div>", unsafe_allow_html=True)

        os.remove("temp_resume1.pdf")
        os.remove("temp_resume2.pdf")

# Individual Resume Analysis
with tab2:
    st.subheader("Upload a Resume for Analysis")
    uploaded_file = st.file_uploader("Upload Resume", type="pdf", key="single")

    if uploaded_file:
        with open("temp_single.pdf", "wb") as f:
            f.write(uploaded_file.read())

        text = extract_text_from_pdf("temp_single.pdf")
        contact_info = extract_contact_info(text)
        summary = generate_structured_summary(text)

        st.markdown("### 📄 Summary")
        st.markdown(f"<div style='background:#f1f1f1;padding:10px;border-radius:8px;'>{summary}</div>", unsafe_allow_html=True)

        st.markdown("### 📇 Contact Information")
        st.write(f"📧 Email: {contact_info.get('Email')}")
        st.write(f"📱 Phone: {contact_info.get('Phone')}")
        st.write(f"🔗 LinkedIn: {contact_info.get('LinkedIn')}")

        keywords = ["python", "machine learning", "data science", "azure", "sql", "react", "cloud", "tensorflow"]
        matched = keyword_match(text, keywords)
        unmatched = [kw for kw in keywords if kw not in matched]
        score = calculate_score(matched, len(keywords), len(text))
        polarity, subjectivity = analyze_sentiment(text)

        st.markdown("### 📊 Analysis")
        st.metric("Score", f"{score}/100")
        st.metric("Sentiment Polarity", f"{polarity:.2f}")
        st.metric("Subjectivity", f"{subjectivity:.2f}")
        st.success(f"Matched Keywords: {', '.join(matched)}")
        st.warning(f"Unmatched Keywords: {', '.join(unmatched)}")

        os.remove("temp_single.pdf")

# JD Matching
with tab3:
    st.subheader("Match Resume to Job Description")
    jd_text = st.text_area("Paste the job description here:")

    resume_file = st.file_uploader("Upload Resume", type="pdf", key="jd")
    if resume_file and jd_text:
        with open("temp_jd_resume.pdf", "wb") as f:
            f.write(resume_file.read())

        resume_text = extract_text_from_pdf("temp_jd_resume.pdf")
        match_score, missing = match_job_description(resume_text, jd_text)

        st.metric("Match Score", f"{match_score:.1f}%")
        if missing:
            st.warning(f"Missing Keywords: {', '.join(missing)}")
        else:
            st.success("Your resume matches the job description well!")

        os.remove("temp_jd_resume.pdf")
