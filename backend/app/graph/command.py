import json
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser

from app.tools.commands import COMMAND_REGISTRY
from app.prompts.command import COMMAND_SYSTEM_PROMPT
from app.graph.state import ImageAgentState, PlanStep
from pydantic import BaseModel


def build_command_prompt(
    step: PlanStep,
    input_path: str,
    output_path: str,
    schema: dict,
) -> str:
    return f"""
Step to execute:
{step.reason}

Operation:
{step.operation}

Input image:
{input_path}

Output image:
{output_path}

Command schema:
{json.dumps(schema, indent=2)}
""".strip()


def command_node(
    state: ImageAgentState,
    llm,
) -> BaseModel:
    step = state.plan[state.current_step_index]
    if step.operation not in COMMAND_REGISTRY:
        raise ValueError(f"Unsupported operation: {step.operation}")

    CommandModel = COMMAND_REGISTRY[step.operation]
    parser = PydanticOutputParser(pydantic_object=CommandModel)

    input_path = state.current_input_path
    output_path = state.next_output_path()

    messages = [
        SystemMessage(content=COMMAND_SYSTEM_PROMPT),
        HumanMessage(
            content=build_command_prompt(
                step=step,
                input_path=input_path,
                output_path=output_path,
                schema=CommandModel.model_json_schema(),
            )
        ),
    ]

    response = llm.invoke(messages)

    try:
        command = parser.parse(response.content)
    except Exception as e:
        raise ValueError(f"Invalid command generated: {e}")

    return command
