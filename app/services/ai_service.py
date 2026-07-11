from google import genai

from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def analyze_portfolio(risk_summary: dict):

    prompt = f"""
You are a senior financial analyst.

Analyze the following investment portfolio.

Portfolio Summary:
{risk_summary}

Provide:

1. Overall Risk Level (Low / Medium / High)

2. Strengths

3. Weaknesses

4. Diversification Suggestions

5. Investment Recommendation

Keep the response concise and professional.
"""

    response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt,
    )

    return response.text if response.text else "No analysis generated."