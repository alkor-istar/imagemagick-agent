from app.graph.state import ImageAgentState, PlanStep


def has_more_steps(state: ImageAgentState) -> bool:
    return state.plan is not None and state.current_step_index < len(state.plan)


def get_current_step(state: ImageAgentState) -> PlanStep:
    return state.plan[state.current_step_index]


def advance_state_node(state: ImageAgentState) -> ImageAgentState:
    state.current_step_index += 1
    print("Advancing state")

    if state.current_output_path and state.current_step_index < len(state.plan):
        state.current_input_path = state.current_output_path
        state.current_output_path = None

    return state
