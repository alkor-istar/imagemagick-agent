from app.graph.state import ImageAgentState
from langchain_core.output_parsers import PydanticOutputParser
from pathlib import Path
from app.tools.commands import ResizeCommand
from app.tools.imagemagick import resize_image


def command_node(state, llm):
    parser = PydanticOutputParser(pydantic_object=ResizeCommand)

    prompt = f"""
You are an image editing compiler.

Your task:
Convert the plan into a SINGLE image operation.

Rules:
- Output MUST be valid JSON
- Do NOT include explanations
- Use only the allowed schema
- Paths must be relative
- Never invent files
- If the request is ambiguous, choose the safest option

Allowed schema: {parser.get_format_instructions()}

Plan:
{state.plan}
"""

    try:
        response = llm.invoke(prompt)
        command = parser.parse(response)
        return {"command": command.dict()}
    except Exception as e:
        return {"error": f"Command generation failed: {e}"}


def execute_node(state):
    try:
        cmd = state.command

        input_path = Path(state.input_path)
        output_path = Path("images/output") / f"out_{Path(state.input_path).name}"

        resize_image(
            input_path=input_path,
            output_path=output_path,
            width=cmd["width"],
            height=cmd["height"],
        )

        return {"result_path": str(output_path)}

    except Exception as e:
        return {"error": f"Execution failed: {e}"}
