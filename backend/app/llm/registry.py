from app.llm.gemini import GeminiClient
from app.llm.base import LLMClient
from app.config import Settings


def get_llm_client(settings: Settings) -> LLMClient:
    provider = settings.llm_provider.lower()

    if provider == "gemini":
        return GeminiClient(
            api_key=settings.google_api_key,
            model=settings.gemini_model,
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")
