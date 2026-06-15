from graph.state import AgentState
from tools.subscription_tool import get_subscription_status


def subscription_agent(state: AgentState):
    decision = state.get(
    "planner_decision",
    {}
)

    if not decision.get(
        "subscription",
        False
    ):

        state["investigation_steps"].append(
            "Subscription Agent skipped"
        )

        return state

    customer_id = state["customer_id"]

    status = get_subscription_status(customer_id)
    state["investigation_steps"].append(
    f"Subscription status is {status}"
)
    state["subscription_status"] = status

    return state