import streamlit as st
import pandas as pd
from gap_analysis import analyze_gap
from my_skills import MY_SKILLS

st.set_page_config(page_title="Skill Gap Analyzer", page_icon="🎯")

st.title("🎯 Skill Gap Analyzer")
st.write("See how your skills compare against real job postings.")

st.subheader("Your current skills (placeholder for now)")
st.write(", ".join(MY_SKILLS))

report_df = analyze_gap("jobs_with_skills.csv", MY_SKILLS)

st.subheader("⚠️ Skills You're Missing (sorted by demand)")
missing = report_df[report_df["you_have_it"] == False]
st.dataframe(missing)

st.subheader("✅ Skills You Already Have")
have = report_df[report_df["you_have_it"] == True]
st.dataframe(have)

st.subheader("📊 Top Skills by Market Demand")
st.bar_chart(report_df.set_index("skill")["demand_pct"].head(15))

st.subheader("📋 Full Report")
st.dataframe(report_df)