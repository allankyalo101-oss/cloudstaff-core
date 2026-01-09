import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
EVENTS_FILE = os.path.join(BASE_DIR, "events", "events.jsonl")

os.makedirs(os.path.dirname(EVENTS_FILE), exist_ok=True)

def log_event(client, action, category, amount=0.0):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "client": client,
        "action": action,
        "category": category,
        "amount": float(amount)
    }
    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

def load_events():
    if not os.path.exists(EVENTS_FILE):
        return []
    with open(EVENTS_FILE, "r") as f:
        return [json.loads(line) for line in f]
