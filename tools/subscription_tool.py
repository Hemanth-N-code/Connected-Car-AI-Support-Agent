import json


def get_subscription_status(customer_id):

    with open("data/subscriptions.json") as f:
        data = json.load(f)

    customer = data.get(customer_id)

    if customer:
        return customer["status"]

    return "unknown"