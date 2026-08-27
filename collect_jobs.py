import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv

# Load the API keys from your .env file
load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

COUNTRY = "in"          # India
ROLE = "software engineer intern"   # change this later to try other roles
PAGES = 5                # each page returns ~20 jobs, so 5 pages = ~100 jobs

def fetch_jobs(role, pages):
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
            print(f"Error on page {page}: {response.status_code}")
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

        print(f"Fetched page {page}, total jobs so far: {len(all_jobs)}")
        time.sleep(1)

    return pd.DataFrame(all_jobs)

if __name__ == "__main__":
    df = fetch_jobs(ROLE, PAGES)
    df.to_csv("raw_jobs.csv", index=False)
    print(f"\nDone! Saved {len(df)} job postings to raw_jobs.csv")