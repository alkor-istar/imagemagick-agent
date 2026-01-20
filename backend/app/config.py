from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()


class Settings(BaseModel):
    google_api_key: str
    llm_provider: str = "gemini"
    gemini_model: str = "gemini-2.5-flash-lite"

    cors_origins: List[str] = []

    class Config:
        env_file = ".env"


def load_settings() -> Settings:
    return Settings(google_api_key=os.environ["GOOGLE_API_KEY"])
