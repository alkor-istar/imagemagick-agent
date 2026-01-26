from langgraph.graph import StateGraph, END
from .state import ImageAgentState
from .planner import planner_node
from .command import command_node
from .executor import executor_node
from .debug import debug_node
from .iterator import advance_state_node, has_more_steps


def route_after_planner(state: ImageAgentState) -> str:
    if not state.plan or len(state.plan) == 0:
        return "done"
    return "command"


def route_after_advance(state: ImageAgentState) -> str:
    if has_more_steps(state):
        return "command"
    return "done"


def build_graph(llm):
    graph = StateGraph(ImageAgentState)

    graph.add_node("planner", lambda s: planner_node(s, llm))
    graph.set_entry_point("planner")
    graph.add_node("command", lambda s: command_node(s, llm))
    graph.add_node("execute", executor_node)
    graph.add_node("advance", advance_state_node)

    graph.set_entry_point("planner")

    graph.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "command": "command",
            "done": END,
        },
    )

    graph.add_edge("command", "execute")
    graph.add_edge("execute", "advance")

    graph.add_conditional_edges(
        "advance",
        route_after_advance,
        {
            "command": "command",
            "done": END,
        },
    )

    return graph.compile()
