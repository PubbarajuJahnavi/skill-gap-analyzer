import pandas as pd
import ast
from collections import Counter
from my_skills import MY_SKILLS

def analyze_gap(jobs_csv_path, my_skills):
    df = pd.read_csv(jobs_csv_path)

    # extracted_skills was saved as text like "['python', 'sql']"
    # ast.literal_eval turns that text back into a real Python list
    df["extracted_skills"] = df["extracted_skills"].apply(ast.literal_eval)

    all_skills = []
    for skill_list in df["extracted_skills"]:
        all_skills.extend(skill_list)

    demand_counts = Counter(all_skills)
    total_jobs = len(df)

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

if __name__ == "__main__":
    report_df = analyze_gap("jobs_with_skills.csv", MY_SKILLS)
    print(report_df.to_string())
    report_df.to_csv("gap_report.csv", index=False)
    print("\nSaved full report to gap_report.csv")