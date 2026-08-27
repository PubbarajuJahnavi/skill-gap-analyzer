import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

COUNTRY = "in"
PAGES_PER_ROLE = 8   # ~160 jobs per domain

# Each domain maps to a real search term used on Adzuna
DOMAINS = {
    "Software / CSE": "software engineer",
    "Web Development": "web developer",
    "Data Science / AI-ML": "data scientist",
    "Cloud / DevOps": "devops engineer",
    "Mechanical Engineering": "mechanical engineer",
    "Civil Engineering": "civil engineer",
    "Electrical Engineering": "electrical engineer",
    "Electronics / ECE": "electronics engineer",
    "Core Engineering (General)": "engineering graduate trainee"
}

def fetch_jobs_for_role(role, pages):
    all_jobs = []
    for page in range(1, pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": role,
            "results_per_page": 20
        }
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Error on page {page} for '{role}': {response.status_code}")
            continue

        data = response.json()
        for job in data.get("results", []):
            all_jobs.append({
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "description": job.get("description"),
                "location": job.get("location", {}).get("display_name"),
                "date_posted": job.get("created")
            })
        time.sleep(1)

    return all_jobs

if __name__ == "__main__":
    all_data = []

    for domain_label, search_term in DOMAINS.items():
        print(f"\nFetching jobs for domain: {domain_label} (searching '{search_term}')")
        jobs = fetch_jobs_for_role(search_term, PAGES_PER_ROLE)
        for job in jobs:
            job["domain"] = domain_label   # tag each job with its domain
        all_data.extend(jobs)
        print(f"  -> Got {len(jobs)} jobs for {domain_label}")

    df = pd.DataFrame(all_data)
    df.to_csv("raw_jobs.csv", index=False)
    print(f"\nDone! Saved {len(df)} total job postings across {len(DOMAINS)} domains to raw_jobs.csv")