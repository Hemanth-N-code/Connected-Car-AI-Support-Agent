import json

from utils.llm import llm
import time


def investigation_agent(state):

    query = state["customer_query"]

    kb = state.get(
        "kb_context",
        ""
    )

    prompt = f"""
You are a senior automotive diagnostic engineer.

Customer Query:
{state["customer_query"]}

Issue Category:
{state["issue_category"]}

CRM Data:
{state.get("crm_data", {})}

Telematics Data:
{state.get("telematics_data", {})}

Subscription Status:
{state.get("subscription_status", "unknown")}

Knowledge Base:
{state["kb_context"]}

IMPORTANT:

You MUST identify ONE most likely root cause.

Never return multiple possible causes.

Use this priority:

1. Real evidence from CRM/Telematics/Subscription
2. Knowledge Base symptoms
3. Most likely cause from KB

If evidence is missing,
select the MOST LIKELY root cause from the KB.

Return a single root cause only.

Also provide:

- confidence
- evidence_used

Return ONLY valid JSON:

{{
  "root_cause":"",
  "confidence":0.0,
  "evidence_used":[],
  "resolution":""
}}
"""
    start = time.time()
    response = llm.invoke(prompt)
    print(
    "\nInvestigation Agent Time:",
    round(time.time() - start, 2),
    "seconds"
)

    text = (
        response.content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        result = json.loads(text)

        state["root_cause"] = result["root_cause"]

        state["root_cause_confidence"] = result.get(
            "confidence",
            0
        )

        state["evidence_used"] = result.get(
            "evidence_used",
            []
        )

        state["resolution"] = result["resolution"]

    except:

        state["root_cause"] = (
            "Unknown"
        )

        state["resolution"] = (
            "Escalate to technician"
        )

    state["investigation_steps"].append(
        f"Root cause identified as {state['root_cause']}"
    )

    state["investigation_steps"].append(
        "Resolution generated"
    )

    return state