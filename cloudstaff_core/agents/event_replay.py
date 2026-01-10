import json
import hashlib
from pathlib import Path

EVENTS_PATH = Path("cloudstaff_core/storage/events/events.jsonl")


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def canonical_event_string(event: dict) -> str:
    filtered = {
        k: event[k]
        for k in sorted(event.keys())
        if k not in ("event_hash", "prev_hash")
    }
    return json.dumps(filtered, sort_keys=True, separators=(",", ":"))


def resolve_client(event: dict, line: int) -> str:
    """
    Canonical client resolver.
    Supports historical schema drift.
    """

    client = event.get("client")
    client_name = event.get("client_name")

    if client and client_name:
        if client != client_name:
            raise RuntimeError(
                f"Client ambiguity at line {line}: "
                f"client='{client}' vs client_name='{client_name}'"
            )
        return client

    if client:
        return client

    if client_name:
        return client_name

    raise RuntimeError(f"Missing client identity at line {line}")


def semantic_apply(event: dict, state: dict, line: int):
    client = resolve_client(event, line)
    amount = float(event.get("amount", 0))

    action = str(event.get("action", "")).lower()
    category = str(event.get("category", "")).lower()

    if category == "invoice" and "issued" in action:
        state[client] = state.get(client, 0) + amount

    elif category == "invoice" and "payment" in action:
        state[client] = state.get(client, 0) - amount

    else:
        raise RuntimeError(
            f"Unrecognized semantic event at line {line}: "
            f"category='{category}', action='{action}'"
        )


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
                    f"expected {prev_hash}, found {event['prev_hash']}"
                )

            event_str = canonical_event_string(event)
            expected_hash = sha256(prev_hash + event_str)

            if event["event_hash"] != expected_hash:
                raise RuntimeError(
                    f"TAMPER DETECTED at line {index}: hash mismatch"
                )

            semantic_apply(event, state, index)
            prev_hash = event["event_hash"]

    return state
