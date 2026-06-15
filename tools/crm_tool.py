import json

def get_customer_info(customer_id):

    with open("data/crm.json") as f:
        data = json.load(f)

    return data.get(customer_id, {})