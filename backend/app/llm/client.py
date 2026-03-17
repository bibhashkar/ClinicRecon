import asyncio

from openai import OpenAI, RateLimitError

from app.core.config import settings


class LLMRateLimitError(Exception):
    """Raised when the LLM provider returns a rate limit response."""


async def call_llm(system: str, user: str) -> str:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.OPENROUTER_API_KEY,
    )

    max_retries = 3
    base_delay = 1.0

    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model="nvidia/nemotron-3-super-120b-a12b:free",
                messages=[
                    {
                        "role": "user",
                        "content": f"{system}\n\n{user}",
                    }
                ],
                extra_body={"reasoning": {"enabled": True}},
            )

            response_message = response.choices[0].message
            print(f"Assistant's response: {response_message.content}")

            return f"{response_message.content}"

        except RateLimitError as e:
            if attempt == max_retries:
                raise LLMRateLimitError(
                    "LLM rate limit reached after retries."
                ) from e

            delay = base_delay * (2 ** (attempt - 1))
            print(
                f"Rate limit hit (attempt {attempt}/{max_retries}). Retrying in {delay}s..."
            )
            await asyncio.sleep(delay)
            continue

        except Exception as e:
            # Log other errors and return empty JSON to keep downstream logic stable.
            print(f"LLM API call failed: {e}. Returning empty response.")
            return "{}"

    return "{}"
