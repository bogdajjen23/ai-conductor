import json

with open("data/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

def route_request(user_input):
    for assistant in config["assistants"]:
        for kw in assistant["keywords"]:
            if kw in user_input.lower():
                return {
                    "assistant": assistant["id"],
                    "assistant_name": assistant["name"],
                    "question": user_input
                }
    return {
        "assistant": "0",
        "assistant_name": "Общий ассистент",
        "question": user_input
    }
