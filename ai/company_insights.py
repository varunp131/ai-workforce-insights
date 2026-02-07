import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_company_insights(summary):
    
    import streamlit as st
    st.write("Groq call happening now...")

    prompt = f"""
You are an AI workforce financial analyst for an employee benefits platform like Maji.

Company summary:
- Total employees: {summary['total_employees']}
- High risk employees: {summary['high_risk']}
- Average savings months: {summary['avg_savings_months']}
- Average salary: {summary['avg_salary']}

Write a short executive report for HR leaders.

Include:
1. Key financial stress insight
2. Main employer risk
3. Benefit optimisation opportunity
4. Estimated business impact

Keep it concise and professional.
Do NOT invent metrics not provided.
"""

    completion = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300,
    )

    return completion.choices[0].message.content
