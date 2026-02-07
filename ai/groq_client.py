from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv
from groq import Groq

_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path)


def get_recommendation(employee: Dict[str, Any]) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set. Add it to ai/.env and restart.")

    client = Groq(api_key=api_key)

    prompt = (
        "You are an AI financial wellbeing assistant for an employee benefits platform.\n\n"
        f"Employee data:\n{employee}\n\n"
        "Provide:\n"
        "1. Risk explanation\n"
        "2. Benefit optimisation suggestions\n"
        "3. Coaching plan\n"
        "4. Employer insight\n"
    )

    completion = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300,
    )

    return completion.choices[0].message.content.strip()
