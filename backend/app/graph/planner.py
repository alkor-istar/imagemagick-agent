from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from app.graph.state import ImageAgentState, PlanStep
from typing import List
from app.prompts.planner import PLANNER_SYSTEM_PROMPT
from pydantic import BaseModel


class PlanOutput(BaseModel):
    steps: List[PlanStep]


def build_planner_prompt(state: ImageAgentState) -> str:
    md = state.image_metadata
    return f"""
User request:
{state.user_request}

Image metadata:
- Width: {md.width}px
- Height: {md.height}px
- Format: {md.format}
- Mode: {md.mode}
"""


def planner_node(state: ImageAgentState, llm) -> ImageAgentState:
    print("planner node")
    parser = PydanticOutputParser(pydantic_object=PlanOutput)

    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=build_planner_prompt(state)),
    ]

    response = llm.invoke(messages)

    plan = parser.parse(response)

    state.plan = plan.steps
    return state
