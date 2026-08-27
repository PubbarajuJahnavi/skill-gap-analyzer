import pandas as pd
import re
from skills_list import SKILLS_TAXONOMY

def extract_skills(text, skills_taxonomy):
    if not isinstance(text, str):
        return []
    text = text.lower()
    found = []
    for skill in skills_taxonomy:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found.append(skill)
    return found

if __name__ == "__main__":
    df = pd.read_csv("raw_jobs.csv")
    df["extracted_skills"] = df["description"].apply(
        lambda x: extract_skills(x, SKILLS_TAXONOMY)
    )
    df.to_csv("jobs_with_skills.csv", index=False)

    print("Sample results:")
    print(df[["title", "extracted_skills"]].head(10).to_string())