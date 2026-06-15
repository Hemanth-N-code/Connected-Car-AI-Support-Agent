from langgraph.graph import StateGraph

from graph.state import AgentState
from agents.intent_agent import intent_agent
from agents.subscription_agent import subscription_agent
from agents.crm_agent import crm_agent
from agents.telematics_agent import telematics_agent
from agents.knowledge_agent import knowledge_agent
from agents.investigation_agent import investigation_agent

def build_graph():

    builder = StateGraph(AgentState)
       
    builder.add_node(
        "intent",
        intent_agent
    )

    builder.add_node(
        "subscription",
        subscription_agent
    )

    builder.add_node(
    "investigation",
    investigation_agent
)
    
    builder.add_node("crm", crm_agent)

    builder.add_node(
    "telematics",
    telematics_agent
)
    builder.add_node(
    "knowledge",
    knowledge_agent
)
 

    
    builder.set_entry_point("intent")

    builder.add_edge(
    "intent",
    "crm"
)

    builder.add_edge(
    "crm",
    "telematics"
)

    builder.add_edge(
    "telematics",
    "subscription"
)

    builder.add_edge(
    "subscription",
    "knowledge"
)

    builder.add_edge(
    "knowledge",
    "investigation"
)

    builder.set_finish_point(
    "investigation"
)

    return builder.compile()