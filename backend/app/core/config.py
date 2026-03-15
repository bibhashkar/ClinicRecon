from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""  # fallback
    OPENAI_API_KEY: str = ""  # fallback
    OPENROUTER_API_KEY: str = ""  # fallback
    API_KEY: str
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()