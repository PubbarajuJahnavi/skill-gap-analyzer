# 🎯 Skill Gap Analyzer

A tool that pulls real job postings from the web, extracts required skills using NLP-based fuzzy matching, and compares them against a user's resume/GitHub to show exactly what to learn next — built for B.Tech students across all branches, not just CSE.

**Live demo:** https://skill-gap-analyzer-hkxvsvgbaqsgqtvsw4hukd.streamlit.app/

## Why I Built This
As a 3rd-year CSE student prepping for placements, I wanted to know exactly which skills were actually in demand for the roles I'm targeting, instead of guessing. So I built the tool I wish I had — then expanded it so students from other branches (Mechanical, Civil, Electrical, ECE) could use it too.

## Features
- 📄 **Resume Upload** — parses your PDF resume and extracts your skills automatically
- 🎯 **Domain Selection** — compare against 9 different engineering domains (CSE, Web Dev, Data Science, DevOps, Mechanical, Civil, Electrical, ECE, Core Engineering)
- 🔍 **Fuzzy Skill Matching** — catches skill variations (e.g., "React.js", "ReactJS", "React") using similarity matching, not just exact keywords
- 📊 **Priority Scoring** — ranks missing skills by a weighted score combining in-domain demand and cross-domain usefulness, so you know what to learn first
- 🔗 **GitHub-Proven Skills** — checks your GitHub repos and flags which of your skills are backed by actual code, not just listed on paper
- 📥 **PDF Export** — download your personalized gap report to keep or share

## How It Works
1. **Data Collection** — Pulls live job postings from the Adzuna API across 9 target domains
2. **Skill Extraction** — Scans each job description using exact + fuzzy matching against a curated, multi-domain skills taxonomy
3. **Resume/GitHub Parsing** — Extracts your current skills from an uploaded resume and cross-references them with your GitHub repo languages
4. **Gap Analysis** — Calculates a priority score per skill (demand within domain + cross-domain relevance) and compares it against your current skills
5. **Dashboard** — Displays an interactive report: prioritized missing skills, your in-demand skills, GitHub-proven badges, and a downloadable PDF

## Tech Stack
- **Python** — core logic
- **Adzuna API** — real job posting data across domains
- **RapidFuzz** — fuzzy skill matching
- **Pandas** — data processing and aggregation
- **pdfplumber** — resume PDF parsing
- **GitHub REST API** — proven skills detection
- **fpdf2** — PDF report generation
- **Streamlit** — interactive web dashboard
- **Streamlit Community Cloud** — free deployment

## Run It Locally
```bash
git clone https://github.com/PubbarajuJahnavi/skill-gap-analyzer.git
cd skill-gap-analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python collect_jobs.py
python extract_skills.py
streamlit run app.py
```

## Current Limitations & Next Steps
- Skill taxonomy is manually curated; could expand further with more branch-specific skills based on user feedback
- Currently pulls a fixed snapshot of job data; a future version could refresh data on a schedule and show demand trends over time
- Priority scoring weights (70% domain demand / 30% cross-domain spread) are a starting heuristic — could be tuned based on real outcomes

## Feedback
Built and shared with classmates for real testing — actively improving based on feedback. Feel free to open an issue or reach out if you spot a bug or have a suggestion.