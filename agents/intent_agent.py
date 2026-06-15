import json
import time

from utils.llm import llm


def intent_agent(state):

    query = state["customer_query"]

    prompt = f"""
You are an automotive support classifier.

Classify the complaint and decide which systems need investigation.

Issue Categories:

1. app_pairing
2. subscription_issue
3. connectivity_issue
4. infotainment_issue
5. door_lock_issue
6. remote_control_issue
7. vehicle_start_issue
8. charging_issue
9. navigation_issue
10. unknown

Planner Rules:

- app_pairing -> CRM, Telematics, Subscription
- remote_control_issue -> CRM, Telematics, Subscription
- door_lock_issue -> CRM only
- vehicle_start_issue -> CRM, Telematics
- charging_issue -> CRM, Telematics
- navigation_issue -> CRM, Telematics
- connectivity_issue -> CRM, Telematics
- infotainment_issue -> CRM, Telematics
- subscription_issue -> CRM, Subscription

Return ONLY valid JSON.

Example:

{{
    "issue_category":"app_pairing",
    "severity":"medium",
    "confidence":0.95,

    "planner_decision": {{
        "crm": true,
        "telematics": true,
        "subscription": true
    }}
}}

Complaint:
{query}
"""

    start = time.time()

    response = llm.invoke(prompt)

    print(
        "\nIntent+Planner Agent Time:",
        round(time.time() - start, 2),
        "seconds"
    )

    clean_text = (
        response.content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    print("\nRAW RESPONSE:")
    print(clean_text)

    result = json.loads(clean_text)

    state["issue_category"] = result["issue_category"]
    state["severity"] = result["severity"]
    state["confidence"] = result["confidence"]

    state["planner_decision"] = result["planner_decision"]

    if "investigation_steps" not in state:
        state["investigation_steps"] = []

    state["investigation_steps"].append(
        f"Intent Agent classified issue as {result['issue_category']}"
    )

    state["investigation_steps"].append(
        f"Planner selected: {result['planner_decision']}"
    )

    return state