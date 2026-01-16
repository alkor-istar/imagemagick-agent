from langgraph.graph import StateGraph
from .state import ImageAgentState
from .nodes import plan_node, command_node, execute_node


def build_graph(llm):
    graph = StateGraph(ImageAgentState)

    graph.add_node("plan", lambda s: plan_node(s, llm))
    graph.add_node("command", lambda s: command_node(s, llm))
    graph.add_node("execute", execute_node)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "command")
    graph.add_edge("command", "execute")

    return graph.compile()
