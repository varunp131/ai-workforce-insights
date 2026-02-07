import pandas as pd
import sys, os

sys.path.append(os.path.dirname(__file__))

from models.risk_model import calculate_risk
from ai.groq_client import get_recommendation

df = pd.read_csv("data/employees.csv")

row = df.iloc[0].to_dict()

risk = calculate_risk(row)
row.update(risk)

print("Risk:", risk)
print("\nAI OUTPUT:\n")
print(get_recommendation(row))
