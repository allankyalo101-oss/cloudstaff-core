import json
from pathlib import Path

EVENTS_PATH = Path("cloudstaff_core/storage/events/events.jsonl")
SNAPSHOT_PATH = Path("cloudstaff_core/storage/snapshots/latest.json")

# Pending events in memory
pending_events = []

# -------------------------
# Append a new event
# -------------------------
def add_event(event):
    global pending_events
    pending_events.append(event)

# -------------------------
# Flush all events to disk
# -------------------------
def flush_events():
    global pending_events
    if not pending_events:
        return
    with open(EVENTS_PATH, "a") as f:
        for event in pending_events:
            f.write(json.dumps(event) + "\n")
    pending_events.clear()  # memory cleared after persistence

# -------------------------
# Write snapshot
# -------------------------
def write_snapshot():
    # Ensure all events are flushed first
    flush_events()

    # Read full ledger state from events
    ledger_state = {}
    if EVENTS_PATH.exists():
        with open(EVENTS_PATH, "r") as f:
            for line in f:
                e = json.loads(line)
                client = e["client_name"]
                if client not in ledger_state:
                    ledger_state[client] = {"invoiced": 0.0, "paid": 0.0, "balance": 0.0}
                if e["type"] == "Invoice":
                    ledger_state[client]["invoiced"] += e["amount"]
                    ledger_state[client]["balance"] += e["amount"]
                elif e["type"] == "Payment":
                    ledger_state[client]["paid"] += e["amount"]
                    ledger_state[client]["balance"] -= e["amount"]

    # Write snapshot
    with open(SNAPSHOT_PATH, "w") as f:
        json.dump(ledger_state, f, indent=4)

    print("Snapshot written. Events persisted.")

# -------------------------
# Execution
# -------------------------
if __name__ == "__main__":
    flush_events()
    write_snapshot()
