import streamlit as st
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import plotly.express as px

from models.risk_model import calculate_risk
from ai.groq_client import get_recommendation
from ai.company_insights import generate_company_insights

# ---------- ENV ----------
_env_path = Path(__file__).resolve().parent / "ai" / ".env"
load_dotenv(_env_path)

# ---------- PAGE ----------
st.set_page_config(page_title="AI Workforce Insights", layout="wide")
st.title("AI Workforce Financial Insights Dashboard")
st.markdown(
"AI-powered dashboard that analyzes employee financial wellness and generates company-level risk insights for HR teams."
)

# ---------- DEMO DATA ----------
def load_demo_data():
    return pd.DataFrame(
        [
            {
                "employee_id": 1,
                "name": "Amit",
                "salary": 60000,
                "savings": 20000,
                "debt": 10000,
                "benefits_used": "yes",
            },
            {
                "employee_id": 2,
                "name": "Sara",
                "salary": 45000,
                "savings": 5000,
                "debt": 20000,
                "benefits_used": "no",
            },
            {
                "employee_id": 3,
                "name": "John",
                "salary": 80000,
                "savings": 40000,
                "debt": 5000,
                "benefits_used": "yes",
            },
        ]
    )


if st.button("Load Demo Company Data", key="load_demo"):
    st.session_state["df"] = load_demo_data()
    st.success("Demo data loaded")

# ---------- LOAD DATA ----------
if "df" in st.session_state:
    df = st.session_state["df"]
else:
    try:
        df = pd.read_csv("data/employees.csv")
    except Exception:
        st.warning("No CSV found. Click 'Load Demo Company Data' to run demo.")
        st.stop()

df["benefits_used"] = df["benefits_used"].astype(str)

# ---------- RISK CALC ----------
risk_levels = []
scores = []
savings_months = []

for _, row in df.iterrows():
    r = calculate_risk(row)
    risk_levels.append(r["risk_level"])
    scores.append(r["risk_score"])
    savings_months.append(r["savings_months"])

df["risk_level"] = risk_levels
df["risk_score"] = scores
df["savings_months"] = savings_months

# ---------- COMPANY OVERVIEW ----------
st.header("Employer Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Employees", len(df))
col2.metric("High Risk", int((df["risk_level"] == "HIGH").sum()))
col3.metric("Avg Savings Months", round(df["savings_months"].mean(), 1))

fig = px.pie(df, names="risk_level", title="Risk Distribution")
st.plotly_chart(fig, width="stretch")

# ---------- AI COMPANY INSIGHTS ----------
st.subheader("AI Company Insights")

if st.button("Generate Company AI Insights", key="company_insights"):
    summary = {
        "total_employees": len(df),
        "high_risk": int((df["risk_level"] == "HIGH").sum()),
        "avg_savings_months": float(df["savings_months"].mean()),
        "avg_salary": float(df["salary"].mean()),
    }

    with st.spinner("Analysing workforce..."):
        insights = generate_company_insights(summary)
        st.write(insights)

# ---------- EMPLOYEE VIEW ----------
st.header("Employee Insights")

emp_id = st.selectbox("Select employee", df["employee_id"], key="employee_select")
emp = df[df["employee_id"] == emp_id].iloc[0]

st.json(emp.to_dict())

if st.button("Generate AI Plan", key="employee_plan"):
    with st.spinner("AI thinking..."):
        emp_metrics = calculate_risk(emp)
        payload = {**emp.to_dict(), **emp_metrics}
        result = get_recommendation(payload)
        st.write(result)
