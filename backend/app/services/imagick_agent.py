from app.graph.graph import build_graph
from app.llm.registry import get_llm_client


def build_imagick_agent(settings):
    llm = get_llm_client(settings)
    graph = build_graph(llm)
    return graph
