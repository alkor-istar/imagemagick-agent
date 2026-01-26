from app.graph.state import ImageAgentState
from app.tools.commands import ImageCommand


def executor_node(state: ImageAgentState, command: ImageCommand) -> ImageAgentState:
    # output_path = run_imagemagick(command)
    print("Executing command:", command)
    state.current_output_path = output_path
    return state
