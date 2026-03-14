import anthropic
from openai import OpenAI
from app.core.config import settings

async def call_llm(system: str, user: str, model: str = "claude-3-5-sonnet-20241022") -> str:
    try:
        client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = await client.messages.create(
            model=model,
            max_tokens=800,
            temperature=0.0,
            system=system,
            messages=[{"role": "user", "content": user}]
        )
        print(f"Anthropic API call successful: {response.content[0].text}")
        return response.content[0].text
    except Exception as e:
        print(f"Anthropic API call failed: {e}. Attempting fallback to OpenAI.")
        # Fallback to OpenAI if Anthropic fails (graceful degradation)
        if settings.OPENAI_API_KEY:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=0.0
            )
            return resp.choices[0].message.content
        raise e