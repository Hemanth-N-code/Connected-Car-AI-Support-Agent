import json

def get_vehicle_status(vehicle_id):

    with open("data/telematics.json") as f:
        data = json.load(f)

    return data.get(vehicle_id, {})