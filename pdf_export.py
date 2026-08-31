from fpdf import FPDF

def generate_pdf_report(report_df, domain, my_skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Skill Gap Analysis Report", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Domain: {domain}", ln=True)
    pdf.cell(0, 8, f"Skills entered: {', '.join(my_skills)}", ln=True)
    pdf.ln(5)

    # Missing skills section
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Top Missing Skills (by priority)", ln=True)
    pdf.set_font("Helvetica", "", 10)

    missing = report_df[report_df["you_have_it"] == False].head(15)
    for _, row in missing.iterrows():
        line = f"- {row['skill']} | Priority: {row['priority_score']} | Demand: {row['demand_pct']}%"
        pdf.cell(0, 7, line, ln=True)

    pdf.ln(5)

    # Have skills section
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Your In-Demand Skills", ln=True)
    pdf.set_font("Helvetica", "", 10)

    have = report_df[report_df["you_have_it"] == True]
    for _, row in have.iterrows():
        line = f"- {row['skill']} | Priority: {row['priority_score']} | Demand: {row['demand_pct']}%"
        pdf.cell(0, 7, line, ln=True)

    return bytes(pdf.output())