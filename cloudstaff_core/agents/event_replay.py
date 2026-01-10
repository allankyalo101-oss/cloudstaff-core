import json
import hashlib
from pathlib import Path

EVENTS_PATH = Path("cloudstaff_core/storage/events/events.jsonl")


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def canonical_event_string(event: dict) -> str:
    """
    Deterministic representation for hashing.
    Must match event_chain_guard exactly.
    """
    filtered = {
        k: event[k]
        for k in sorted(event.keys())
        if k not in ("event_hash", "prev_hash")
    }
    return json.dumps(filtered, sort_keys=True, separators=(",", ":"))


def replay_events():
    if not EVENTS_PATH.exists():
        raise RuntimeError("Events file missing")

    state = {}
    prev_hash = "GENESIS"

    with EVENTS_PATH.open("r", encoding="utf-8") as f:
        for index, line in enumerate(f, start=1):
            event = json.loads(line)

            if "event_hash" not in event or "prev_hash" not in event:
                raise RuntimeError(
                    f"INTEGRITY FAILURE: Missing hash fields at line {index}"
                )

            if event["prev_hash"] != prev_hash:
                raise RuntimeError(
                    f"CHAIN BREAK at line {index}: "
                    f"expected prev_hash={prev_hash}, "
                    f"found {event['prev_hash']}"
                )

            event_str = canonical_event_string(event)
            expected_hash = sha256(prev_hash + event_str)

            if event["event_hash"] != expected_hash:
                raise RuntimeError(
                    f"TAMPER DETECTED at line {index}: "
                    f"event_hash mismatch"
                )

            # Apply event
            event_type = event.get("type")

            if event_type == "credit":
                client = event["client"]
                amount = event["amount"]
                state[client] = state.get(client, 0) + amount

            elif event_type == "debit":
                client = event["client"]
                amount = event["amount"]
                state[client] = state.get(client, 0) - amount

            elif event_type == "set":
                client = event["client"]
                amount = event["amount"]
                state[client] = amount

            else:
                raise RuntimeError(
                    f"Unknown event type '{event_type}' at line {index}"
                )

            prev_hash = event["event_hash"]

    return state
