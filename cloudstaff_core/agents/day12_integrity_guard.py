import json
import hashlib
from pathlib import Path

EVENTS_PATH = Path("cloudstaff_core/storage/events/events.jsonl")
SNAPSHOT_PATH = Path("cloudstaff_core/storage/snapshots/latest.json")


def load_events():
    events = []
    if not EVENTS_PATH.exists():
        return events

    with open(EVENTS_PATH, "r") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events


def replay_events():
    """
    Rebuilds state from events.
    Legacy-safe: tolerates missing fields.
    """
    state = {}

    for event in load_events():
        client = event.get("client")
        amount = float(event.get("amount", 0.0))

        if not client:
            continue  # ignore malformed legacy rows

        if client not in state:
            state[client] = {"invoiced": 0.0, "paid": 0.0}

        etype = event.get("type") or event.get("event") or event.get("action")

        if etype == "invoice":
            state[client]["invoiced"] += amount
        elif etype == "payment":
            state[client]["paid"] += amount

    return state


def hash_state(state: dict) -> str:
    payload = json.dumps(state, sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()


def integrity_check():
    print("--- DAY 12 INTEGRITY TEST ---")

    replayed_state = replay_events()
    replay_hash = hash_state(replayed_state)

    if not SNAPSHOT_PATH.exists():
        raise RuntimeError("Snapshot missing — cannot verify integrity")

    with open(SNAPSHOT_PATH, "r") as f:
        snapshot_state = json.load(f)

    snapshot_hash = hash_state(snapshot_state)

    print(f"REPLAY HASH:   {replay_hash}")
    print(f"SNAPSHOT HASH: {snapshot_hash}")

    if replay_hash != snapshot_hash:
        raise RuntimeError("INTEGRITY FAILURE: Snapshot does not match replay")

    print("INTEGRITY VERIFIED: Snapshot matches replayed state")
    print("--- DAY 12 COMPLETE ---")
