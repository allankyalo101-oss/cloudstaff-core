import json
import sqlite3
import hashlib
from pathlib import Path

DB_PATH = "sarah.db"
EVENTS_PATH = Path("cloudstaff_core/storage/events/events.jsonl")
SNAPSHOT_PATH = Path("cloudstaff_core/storage/snapshots/latest_snapshot.json")

def connect_db():
    return sqlite3.connect(DB_PATH)

# -----------------------------
# Event Replay Engine
# -----------------------------
def replay_events():
    state = {}

    if not EVENTS_PATH.exists():
        return state

    with EVENTS_PATH.open() as f:
        for line in f:
            event = json.loads(line)
            name = event["client"]
            amount = event["amount"]
            etype = event["type"]

            if name not in state:
                state[name] = {"invoiced": 0.0, "paid": 0.0}

            if etype == "Invoice":
                state[name]["invoiced"] += amount
            elif etype == "Payment":
                state[name]["paid"] += amount

    return state

# -----------------------------
# Snapshot Loader
# -----------------------------
def load_snapshot():
    if not SNAPSHOT_PATH.exists():
        return {}

    with SNAPSHOT_PATH.open() as f:
        return json.load(f)

# -----------------------------
# Hashing for Integrity
# -----------------------------
def hash_state(state: dict) -> str:
    canonical = json.dumps(state, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()

# -----------------------------
# Integrity Check
# -----------------------------
def integrity_check():
    replayed = replay_events()
    snapshot = load_snapshot()

    replay_hash = hash_state(replayed)
    snapshot_hash = hash_state(snapshot)

    print("REPLAY HASH:  ", replay_hash)
    print("SNAPSHOT HASH:", snapshot_hash)

    if replay_hash != snapshot_hash:
        raise RuntimeError("INTEGRITY FAILURE: Snapshot does not match event replay")

    print("INTEGRITY VERIFIED: Snapshot matches replayed state")

if __name__ == "__main__":
    integrity_check()
