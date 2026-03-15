from openai import OpenAI
from app.core.config import settings


async def call_llm(system: str, user: str) -> str:
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
        )

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
