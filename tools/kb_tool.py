import os


KB_MAPPING = {
    "app_pairing": "app_pairing.txt",
    "subscription_issue": "subscription_issue.txt",
    "connectivity_issue": "connectivity_issue.txt",
    "infotainment_issue": "infotainment_issue.txt",
    "door_lock_issue": "door_lock_issue.txt",
    "remote_control_issue": "remote_control_issue.txt",
    "vehicle_start_issue": "vehicle_start_issue.txt",
    "charging_issue": "charging_issue.txt",
    "navigation_issue": "navigation_issue.txt",
}


def search_knowledge_base(issue_category):

    filename = KB_MAPPING.get(issue_category)

    if not filename:
        filename = "general_troubleshooting.txt"

    filepath = os.path.join(
        "data",
        "kb",
        filename
    )

    try:

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except Exception as e:

        return f"Knowledge base error: {e}"