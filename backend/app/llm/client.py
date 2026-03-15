from openai import OpenAI
from app.core.config import settings


async def call_llm(system: str, user: str) -> str:
    try:
        #         return """
        # {
        # "reconciled_medication": "Metformin 500mg twice daily",
        # "confidence_score": 0.95,
        # "reasoning": "The Hospital EHR record (2000mg/day) from October 2024 is superseded by the Primary Care update (1000mg/day) in January 2025. This reduction is clinically consistent with the patient's eGFR of 45.0, where Metformin dosing is typically capped at 1000mg daily to reduce the risk of lactic acidosis. The Pharmacy fill from late January 2025 confirms the 1000mg total daily dose, likely split into 500mg BID as per the PCP instruction.",
        # "recommended_actions": ["Confirm with the patient that they have transitioned to the lower 500mg BID dose", "Educate patient on the rationale for dose reduction related to kidney function", "Monitor eGFR and creatinine every 3-6 months"],
        # "clinical_safety_check": "PASSED"
        # }
        # """

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
        )

        # First API call with reasoning
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[
                {
                    "role": "user",
                    "content": f"{system}\n\n{user}"
                }
            ],
            extra_body={"reasoning": {"enabled": True}}
        )

        # Extract the assistant message with reasoning_details
        response = response.choices[0].message
        print(f"Assistant's response: {response.content}")

        return f"{response.content}"
    except Exception as e:
        print(
            f"Google Gemini API call failed: {e}. Attempting fallback to Anthropic.")

        return "{}"
