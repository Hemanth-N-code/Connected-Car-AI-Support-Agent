from tools.telematics_tool import (
    get_vehicle_status
)

def telematics_agent(state):

    decision = state.get(
        "planner_decision",
        {}
    )

    # Skip if planner says telematics not needed
    if not decision.get(
        "telematics",
        False
    ):

        state["investigation_steps"].append(
            "Telematics Agent skipped"
        )

        return state

    print("Telematics Agent")
    print(state)

    vehicle = get_vehicle_status(
        state["vehicle_id"]
    )

    state["telematics_data"] = vehicle

    state["investigation_steps"].append(
        "Telematics Agent retrieved vehicle status"
    )

    return state