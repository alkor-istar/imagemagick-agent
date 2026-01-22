def has_more_steps(state: AgentState) -> bool:
    return state.plan is not None and state.current_step_index < len(state.plan)


def get_current_step(state: AgentState) -> PlanStep:
    return state.plan[state.current_step_index]


def advance_state_node(state: AgentState) -> AgentState:
    state.current_step_index += 1

    if state.current_output_path:
        state.current_input_path = state.current_output_path
        state.current_output_path = None

    return state
