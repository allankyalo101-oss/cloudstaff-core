import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
EVENTS_PATH = BASE_DIR / "cloudstaff_core" / "storage" / "events" / "events.jsonl"


def normalize_event(event: dict):
    # Legacy compatibility
    if "client_name" not in event and "client" in event:
        event["client_name"] = event["client"]

    if "type" not in event and "action" in event:
        action = event["action"]
        if "Invoice" in action:
            event["type"] = "Invoice"
        elif "Payment" in action:
            event["type"] = "Payment"
        else:
            return None

    required = ["client_name", "type", "category", "amount"]
    if not all(k in event for k in required):
        return None

    event.setdefault("timestamp", datetime.utcnow().isoformat())
    return event


def replay_events():
    state = {}

    if not EVENTS_PATH.exists():
        return state

    with open(EVENTS_PATH, "r") as f:
        for line in f:
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                continue

            event = normalize_event(raw)
            if event is None:
                continue

            client = event["client_name"]
            etype = event["type"]
            amount = float(event["amount"])

            if client not in state:
                state[client] = {
                    "invoiced": 0.0,
                    "paid": 0.0,
                    "balance": 0.0
                }

            if etype == "Invoice":
                state[client]["invoiced"] += amount
                state[client]["balance"] += amount
            elif etype == "Payment":
                state[client]["paid"] += amount
                state[client]["balance"] -= amount

    return state
