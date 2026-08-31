import pandas as pd
import re
from rapidfuzz import fuzz
from skills_list import SKILLS_TAXONOMY

def normalize(text):
    # Removes dots and hyphens so "React.js", "React-JS", "ReactJS" all become "reactjs"
    return re.sub(r'[\.\-]', '', text.lower())

def extract_skills(text, skills_taxonomy, threshold=85):
    if not isinstance(text, str) or text.strip() == "":
        return []

    text_lower = text.lower()
    found = []

    for skill in skills_taxonomy:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
            continue

        normalized_skill = normalize(skill)
        words_in_text = re.findall(r'\b[\w\.\-\+]+\b', text_lower)
        for word in words_in_text:
            normalized_word = normalize(word)
            if len(normalized_word) < 3:
                continue
            score = fuzz.ratio(normalized_skill, normalized_word)
            if score >= threshold:
                found.append(skill)
                break

    return list(set(found))

if __name__ == "__main__":
    df = pd.read_csv("raw_jobs.csv")
    df["extracted_skills"] = df["description"].apply(
        lambda x: extract_skills(x, SKILLS_TAXONOMY)
    )
    df.to_csv("jobs_with_skills.csv", index=False)

    print("Sample results:")
    print(df[["title", "extracted_skills"]].head(10).to_string())