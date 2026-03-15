from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = ""  # fallback
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()