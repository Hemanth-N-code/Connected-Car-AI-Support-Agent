from tools.crm_tool import get_customer_info

def crm_agent(state):
    print("CRM Agent")
    print(state)
    customer = get_customer_info(
        state["customer_id"]
    )
    state["investigation_steps"].append(
    "CRM Agent retrieved customer history"
)
    state["crm_data"] = customer

    return state