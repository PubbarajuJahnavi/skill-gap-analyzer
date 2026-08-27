import pandas as pd
import ast
from collections import Counter

def analyze_gap(jobs_csv_path, my_skills, domain=None):
    df = pd.read_csv(jobs_csv_path)

    # Filter to just the selected domain, if one is given
    if domain and domain != "All Domains":
        df = df[df["domain"] == domain]

    df["extracted_skills"] = df["extracted_skills"].apply(ast.literal_eval)

    all_skills = []
    for skill_list in df["extracted_skills"]:
        all_skills.extend(skill_list)

    demand_counts = Counter(all_skills)
    total_jobs = len(df)

    if total_jobs == 0:
        return pd.DataFrame(columns=["skill", "demand_pct", "you_have_it", "category"])

    report = []
    for skill, count in demand_counts.most_common():
        demand_pct = round((count / total_jobs) * 100, 1)
        have_it = skill in my_skills

        if have_it and demand_pct > 15:
            category = "Have & In-Demand"
        elif have_it and demand_pct <= 15:
            category = "Have but Low-Demand"
        elif not have_it and demand_pct > 15:
            category = "MISSING & High-Demand (priority)"
        else:
            category = "Missing but Low-Demand"

        report.append({
            "skill": skill,
            "demand_pct": demand_pct,
            "you_have_it": have_it,
            "category": category
        })

    return pd.DataFrame(report).sort_values("demand_pct", ascending=False)