from typing_extensions import TypedDict


class AgentState(TypedDict):

    customer_query: str

    planner_decision: dict

    issue_category: str
    severity: str
    confidence: float

    customer_id: str
    vehicle_id: str

    crm_data: dict
    telematics_data: dict

    subscription_status: str

    kb_context: str

    root_cause: str
    resolution: str
    root_cause_confidence: float

    evidence_used: list

    investigation_steps: list