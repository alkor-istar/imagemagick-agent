from llm.gemini import GeminiClient
from graph.graph import build_graph
from config import load_settings

settings = load_settings()
llm = GeminiClient(api_key=settings.google_api_key, model=settings.gemini_model)
graph = build_graph(llm)

result = graph.invoke(
    {"user_request": "Resize the image cat.jpg to 512x512 and save it"}
)
print(result)
