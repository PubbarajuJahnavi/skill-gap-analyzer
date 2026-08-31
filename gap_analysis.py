import pandas as pd
import ast
from collections import Counter

def analyze_gap(jobs_csv_path, my_skills, domain=None):
    df = pd.read_csv(jobs_csv_path)

    # Keep a copy of all domains before filtering, to calculate cross-domain spread
    full_df = df.copy()
    full_df["extracted_skills"] = full_df["extracted_skills"].apply(ast.literal_eval)

    if domain and domain != "All Domains":
        df = df[df["domain"] == domain]

    df = df.copy()
    df["extracted_skills"] = df["extracted_skills"].apply(ast.literal_eval)

    all_skills = []
    for skill_list in df["extracted_skills"]:
        all_skills.extend(skill_list)

    demand_counts = Counter(all_skills)
    total_jobs = len(df)

    if total_jobs == 0:
        return pd.DataFrame(columns=["skill", "demand_pct", "domain_spread", "priority_score", "you_have_it", "category"])

    # Calculate how many distinct domains each skill appears in (across ALL data, not just filtered)
    skill_to_domains = {}
    for _, row in full_df.iterrows():
        for skill in row["extracted_skills"]:
            skill_to_domains.setdefault(skill, set()).add(row["domain"])

    total_domains = full_df["domain"].nunique()

    report = []
    for skill, count in demand_counts.most_common():
        demand_pct = round((count / total_jobs) * 100, 1)
        domain_spread = len(skill_to_domains.get(skill, set()))
        domain_spread_pct = round((domain_spread / total_domains) * 100, 1) if total_domains > 0 else 0

        # Priority score: weighted combo of demand within domain + how broadly useful it is
        priority_score = round((demand_pct * 0.7) + (domain_spread_pct * 0.3), 1)

        have_it = skill in my_skills

        if have_it and priority_score > 15:
            category = "Have & In-Demand"
        elif have_it and priority_score <= 15:
            category = "Have but Low-Demand"
        elif not have_it and priority_score > 15:
            category = "MISSING & High-Priority"
        else:
            category = "Missing but Low-Priority"

        report.append({
            "skill": skill,
            "demand_pct": demand_pct,
            "domain_spread": f"{domain_spread}/{total_domains} domains",
            "priority_score": priority_score,
            "you_have_it": have_it,
            "category": category
        })

    return pd.DataFrame(report).sort_values("priority_score", ascending=False)