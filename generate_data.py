import pandas as pd
import random
import os

os.makedirs("data", exist_ok=True)

def generate_employee_data(n=120):
    data = []

    for i in range(n):
        salary = random.randint(25000, 120000)
        rent = random.randint(500, 2500)
        savings = random.randint(0, 30000)
        debt = random.randint(0, 20000)
        pension = random.randint(2, 12)
        dependents = random.randint(0, 3)

        benefits = random.choice([
            "none",
            "pension",
            "gym",
            "childcare",
            "pension,gym",
            "pension,childcare"
        ])

        data.append([
            i+1, salary, rent, savings, debt,
            pension, benefits, dependents
        ])

    df = pd.DataFrame(data, columns=[
        "employee_id",
        "salary",
        "rent",
        "savings",
        "debt",
        "pension_percent",
        "benefits_used",
        "dependents"
    ])

    df.to_csv("data/employees.csv", index=False)
    print("Dataset created → data/employees.csv")

generate_employee_data()
