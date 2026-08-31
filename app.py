import streamlit as st
import pandas as pd
import pdfplumber
from gap_analysis import analyze_gap
from skills_list import SKILLS_TAXONOMY
from extract_skills import extract_skills
from github_skills import get_github_skills
from pdf_export import generate_pdf_report

st.set_page_config(page_title="Skill Gap Analyzer", page_icon="🎯")

st.title("🎯 Skill Gap Analyzer")
st.write("Upload your resume and pick a domain to see how your skills compare against real job postings.")

domain_options = [
    "All Domains",
    "Software / CSE",
    "Web Development",
    "Data Science / AI-ML",
    "Cloud / DevOps",
    "Mechanical Engineering",
    "Civil Engineering",
    "Electrical Engineering",
    "Electronics / ECE",
    "Core Engineering (General)"
]
selected_domain = st.selectbox("Which domain are you targeting?", domain_options)
github_username = st.text_input("Your GitHub username (optional, to show proven skills):")
resume_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
manual_skills_input = st.text_area(
    "Or type your skills manually (comma-separated):",
    placeholder="python, sql, git, html, css"
)

def parse_resume_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return extract_skills(text, SKILLS_TAXONOMY)

if st.button("Analyze My Skills"):
    my_skills = []

    if resume_file is not None:
        with st.spinner("Reading your resume..."):
            my_skills = parse_resume_pdf(resume_file)
        st.success(f"Found {len(my_skills)} skills in your resume.")
    elif manual_skills_input.strip() != "":
        my_skills = [s.strip().lower() for s in manual_skills_input.split(",") if s.strip() != ""]
        st.success(f"Using {len(my_skills)} manually entered skills.")
    else:
        st.warning("Please upload a resume or type your skills first.")

    if my_skills:
        github_skills = get_github_skills(github_username) if github_username else set()
        st.write("**Skills detected:** " + ", ".join(my_skills))
        if github_skills:
            proven = [s for s in my_skills if s in github_skills]
            if proven:
                st.info(f"🔗 **GitHub-proven skills:** {', '.join(proven)} — these show up in your actual repos, not just your resume.")
        st.write(f"**Comparing against domain:** {selected_domain}")

        report_df = analyze_gap("jobs_with_skills.csv", my_skills, domain=selected_domain)

        if report_df.empty:
            st.error("No job data found for this domain yet.")
        else:
            st.subheader("⚠️ Skills You're Missing (sorted by priority)")
            missing = report_df[report_df["you_have_it"] == False]
            st.dataframe(missing[["skill", "priority_score", "demand_pct", "domain_spread", "category"]])

            st.subheader("✅ Your Skills That Are In-Demand")
            st.dataframe(report_df[report_df["you_have_it"] == True])

            st.subheader("📊 Top Skills by Market Demand")
            st.bar_chart(report_df.set_index("skill")["demand_pct"].head(15))

            st.subheader("📋 Full Report")
            st.dataframe(report_df)
            pdf_bytes = generate_pdf_report(report_df, selected_domain, my_skills)
            st.download_button(
                label="📥 Download Report as PDF",
                data=pdf_bytes,
                file_name="skill_gap_report.pdf",
                mime="application/pdf"
            )