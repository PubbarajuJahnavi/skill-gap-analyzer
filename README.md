# 🎯 Skill Gap Analyzer

A tool that pulls real job postings from the web, extracts the skills companies are actually asking for using NLP-style text matching, and compares them against a user's current skills to show exactly what to learn next.

**Live demo:** https://skill-gap-analyzer-hkxvsvgbaqsgqtvsw4hukd.streamlit.app/

## Why I Built This
As a 3rd-year CSE student prepping for placements, I wanted to know exactly which skills were actually in demand for the roles I'm targeting, instead of guessing. So I built the tool I wish I had.

## How It Works
1. **Data Collection** — Pulls live job postings from the Adzuna API for a target role (e.g., "Software Engineer Intern")
2. **Skill Extraction** — Scans each job description and extracts mentioned technical skills using keyword/pattern matching against a curated skills taxonomy
3. **Gap Analysis** — Aggregates how often each skill appears across postings (market demand %) and compares it against the user's current skill set
4. **Dashboard** — Displays a live, interactive report: skills you're missing (prioritized by demand), skills you already have, and a market demand chart

## Tech Stack
- **Python** — core logic
- **Adzuna API** — real job posting data
- **Regex-based NLP** — skill extraction from unstructured text
- **Pandas** — data processing and aggregation
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
- Currently uses a placeholder skill list instead of parsing an actual uploaded resume — real resume parsing (PDF upload) is the next planned feature
- Skill extraction uses keyword matching; a future version could use a trained NER model for more accurate extraction of varied phrasing
- Currently tested on one role category; plans to support comparing multiple target roles at once

## Sample Output
The dashboard shows:
- 📊 Top in-demand skills across real job postings
- ⚠️ Skills you're missing, sorted by market demand
- ✅ Skills you already have that are actively in-demand