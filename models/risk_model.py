def calculate_risk(row):
    salary = row.get("salary", 0) or 0
    savings = row.get("savings", 0) or 0
    debt = row.get("debt", 0) or 0
    pension_percent = row.get("pension_percent", 0) or 0

    monthly_income = salary / 12 if salary else 0
    savings_months = savings / monthly_income if monthly_income else 0

    risk_score = 0

    if savings_months < 2:
        risk_score += 2
    elif savings_months < 5:
        risk_score += 1

    if debt > salary * 0.5:
        risk_score += 2
    elif debt > salary * 0.2:
        risk_score += 1

    if pension_percent < 5:
        risk_score += 1

    if risk_score >= 4:
        level = "HIGH"
    elif risk_score >= 2:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_level": level,
        "risk_score": risk_score,
        "savings_months": round(savings_months, 1)
    }
