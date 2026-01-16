from langchain_google_genai import ChatGoogleGenerativeAI
from .base import LLMClient
import os


class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: str):
        self.llm = ChatGoogleGenerativeAI(model=model, api_key=api_key)

    def invoke(self, prompt: str) -> str:
        return self.llm.invoke(prompt).content
