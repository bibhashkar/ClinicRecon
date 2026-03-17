import asyncio
import hashlib

from cachetools import TTLCache
from openai import OpenAI, RateLimitError

from app.core.config import settings


class LLMRateLimitError(Exception):
    """Raised when the LLM provider returns a rate limit response."""


# In-memory cache for identical prompts. For multi-instance deployments, replace
# with a shared cache (e.g., Redis) using the same keying strategy.
_LLM_CACHE = TTLCache(maxsize=1024, ttl=60 * 60 * 24)  # 1 day
_cache_lock = asyncio.Lock()


def _cache_key(system: str, user: str) -> str:
    raw = f"{system}\n\n{user}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


async def call_llm(system: str, user: str) -> str:
    cache_key = _cache_key(system, user)

    async with _cache_lock:
        cached = _LLM_CACHE.get(cache_key)
        if cached is not None:
            print("LLM response retrieved from cache.")
            return cached

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
            result = f"{response_message.content}"
            print(f"Assistant's response: {result}")

            async with _cache_lock:
                _LLM_CACHE[cache_key] = result

            return result

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
