from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    google_api_key: str
    llm_provider: str = "gemini"
    gemini_model: str = "gemini-2.5-flash-lite"
    cors_origins: List[str] = []

    class Config:
        env_file = ".env"


def load_settings() -> Settings:
    return Settings()
