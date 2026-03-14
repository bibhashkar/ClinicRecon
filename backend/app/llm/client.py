import os
from google import genai
from google.genai import types
import anthropic
from openai import OpenAI
from app.core.config import settings


async def call_llm(system: str, user: str) -> str:
    # Set API key for Gemini
    os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY

    print(f"{system}\n\n{user}")

    # Try Google Gemini first
    try:
        # client = genai.Client()
        # response = client.models.generate_content(
        #     model="gemini-3.1-pro-preview",
        #     contents=f"{system}\n\n{user}",
        #     config=types.GenerateContentConfig(
        #         temperature=0.0,
        #         max_output_tokens=800,
        #     )
        # )
        # print(response)
        # print(f"Google Gemini API call successful: {response.text}")
        # return response.text

        return """
{
"reconciled_medication": "Metformin 500mg twice daily",
"confidence_score": 0.95,
"reasoning": "The Hospital EHR record (2000mg/day) from October 2024 is superseded by the Primary Care update (1000mg/day) in January 2025. This reduction is clinically consistent with the patient's eGFR of 45.0, where Metformin dosing is typically capped at 1000mg daily to reduce the risk of lactic acidosis. The Pharmacy fill from late January 2025 confirms the 1000mg total daily dose, likely split into 500mg BID as per the PCP instruction.",
"recommended_actions": ["Confirm with the patient that they have transitioned to the lower 500mg BID dose", "Educate patient on the rationale for dose reduction related to kidney function", "Monitor eGFR and creatinine every 3-6 months"],
"clinical_safety_check": "PASSED"
}
"""

    except Exception as e:
        print(
            f"Google Gemini API call failed: {e}. Attempting fallback to Anthropic.")
        # Fallback to Anthropic
        # try:
        #     client = anthropic.AsyncAnthropic(
        #         api_key=settings.ANTHROPIC_API_KEY)
        #     response = await client.messages.create(
        #         model="claude-3-5-sonnet-20241022",
        #         max_tokens=800,
        #         temperature=0.0,
        #         system=system,
        #         messages=[{"role": "user", "content": user}]
        #     )
        #     print(f"Anthropic API call successful: {response.content[0].text}")
        #     return response.content[0].text
        # except Exception as e:
        #     print(
        #         f"Anthropic API call failed: {e}. Attempting fallback to OpenAI.")
        #     # Fallback to OpenAI if both fail
        #     if settings.OPENAI_API_KEY:
        #         client = OpenAI(api_key=settings.OPENAI_API_KEY)
        #         resp = client.chat.completions.create(
        #             model="gpt-4o",
        #             messages=[{"role": "system", "content": system},
        #                       {"role": "user", "content": user}],
        #             temperature=0.0
        #         )
        #         print(
        #             f"OpenAI API call successful: {resp.choices[0].message.content}")
        #         return resp.choices[0].message.content
        #     raise e
