import json
import hashlib
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
EVENTS_PATH = BASE_DIR / "cloudstaff_core" / "storage" / "events" / "events.jsonl"
SNAPSHOT_DIR = BASE_DIR / "cloudstaff_core" / "storage" / "snapshots"
SNAPSHOT_PATH = SNAPSHOT_DIR / "latest.json"

SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def normalize_event(event: dict):
    """
    Normalize legacy and current event formats into canonical schema.
    Returns None if event is unrecoverable.
    Canonical schema:
        client_name
        type
        category
        amount
        timestamp
    """

    # Legacy → canonical mapping
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

    # Hard validation
    required = ["client_name", "type", "category", "amount"]
    if not all(k in event for k in required):
        return None

    event.setdefault("timestamp", datetime.utcnow().isoformat())
    return event


def write_snapshot():
    state = {}

    if not EVENTS_PATH.exists():
        print("No events found. Snapshot aborted.")
        return

    with open(EVENTS_PATH, "r") as f:
        for line in f:
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                print(f"WARNING: Skipping corrupted JSON line: {line.strip()}")
                continue

            event = normalize_event(raw)
            if event is None:
                print(f"WARNING: Skipping malformed event: {raw}")
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

    snapshot = {
        "generated_at": datetime.utcnow().isoformat(),
        "state": state,
        "hash": hash_state(state)
    }

    with open(SNAPSHOT_PATH, "w") as f:
        json.dump(snapshot, f, indent=2)

    print("Snapshot written. Events persisted.")


def hash_state(state: dict) -> str:
    canonical = json.dumps(state, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


if __name__ == "__main__":
    write_snapshot()
