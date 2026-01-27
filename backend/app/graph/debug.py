from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from app.graph.state import ImageAgentState, PlanStep
from typing import List
from app.prompts.planner import PLANNER_SYSTEM_PROMPT
from pydantic import BaseModel


def debug_node(state: ImageAgentState) -> ImageAgentState:
    print("state", state)

    return state
