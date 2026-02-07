
# ai-workforce-insights
AI dashboard that analyzes employee financial data and generates company-level insights using Groq LLM.

# AI Workforce Insights

Streamlit app for workforce financial risk insights and AI recommendations.

## Setup

1. Install dependencies:
```
python -m pip install -r requirements.txt
python -m pip install altair==4.2.2
```

2. Create `.env` from the example:
```
copy .env.example ai\.env
```

3. Add your Groq API key:
```
GROQ_API_KEY=your_key_here
```

4. Run the app:
```
python -m streamlit run app.py
```

altair==4.2.2
