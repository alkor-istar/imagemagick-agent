import json
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser

from app.tools.commands import COMMAND_REGISTRY
from app.prompts.command import COMMAND_SYSTEM_PROMPT
from app.graph.state import ImageAgentState, PlanStep
from pydantic import BaseModel
from pathlib import Path
from utils.image_utils import extract_metadata


def build_command_prompt(
    step: PlanStep, input_path: str, schema: dict, image_metadata: dict
) -> str:
    return f"""
Step to execute:
{step.reason}

Operation:
{step.operation}

Input image:
{input_path}

Image metadata: 
{image_metadata}

Command schema:
{json.dumps(schema, indent=2)}
""".strip()


def command_node(
    state: ImageAgentState,
    llm,
) -> ImageAgentState:
    print("command node")
    step = state.plan[state.current_step_index]
    if step.operation not in COMMAND_REGISTRY:
        raise ValueError(f"Unsupported operation: {step.operation}")

    CommandModel = COMMAND_REGISTRY[step.operation]
    parser = PydanticOutputParser(pydantic_object=CommandModel)

    input_path = state.current_input_path
    image_metadata = extract_metadata(Path(input_path))

    messages = [
        SystemMessage(content=COMMAND_SYSTEM_PROMPT),
        HumanMessage(
            content=build_command_prompt(
                step=step,
                input_path=input_path,
                schema=CommandModel.model_json_schema(),
                image_metadata=image_metadata,
            )
        ),
    ]

    response = llm.invoke(messages)
    print("Response", response)

    try:
        command = parser.parse(response)
        print("Command:", command)
        state.current_command = command
        return state
    except Exception as e:
        raise ValueError(f"Invalid command generated: {e}")
