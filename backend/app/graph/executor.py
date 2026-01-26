from app.graph.state import ImageAgentState
from app.tools.commands import ImageCommand
from pathlib import Path
from app.tools.imagemagick import run_imagemagick

OUTPUT_DIR = Path("images/output")


def executor_node(state: ImageAgentState) -> ImageAgentState:
    command = state.current_command

    # Do not trust LLM with paths
    input_path = Path(state.current_input_path)
    output_path = OUTPUT_DIR / f"out_{Path(state.current_input_path).name}"
    command.input_path = str(input_path)
    command.output_path = str(output_path)
    state.current_output_path = str(output_path)

    run_imagemagick(command)
    print("Executing command:", state.current_command)
    return state
