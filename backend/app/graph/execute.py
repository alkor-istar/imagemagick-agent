def executor_node(state: AgentState, command: BaseCommand) -> AgentState:
    output_path = run_imagemagick(command)
    state.current_output_path = output_path
    return state
