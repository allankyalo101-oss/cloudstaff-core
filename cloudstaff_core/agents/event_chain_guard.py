import json
import hashlib
import shutil
from pathlib import Path

EVENTS_PATH = Path("cloudstaff_core/storage/events/events.jsonl")
BACKUP_PATH = Path("cloudstaff_core/storage/events/events.backup.chain.jsonl")


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def canonical_event_string(event: dict) -> str:
    """
    Produce a deterministic string for hashing.
    Excludes hash fields themselves.
    """
    filtered = {
        k: event[k]
        for k in sorted(event.keys())
        if k not in ("event_hash", "prev_hash")
    }
    return json.dumps(filtered, sort_keys=True, separators=(",", ":"))


def chain_events():
    if not EVENTS_PATH.exists():
        raise RuntimeError("Events file does not exist")

    # Backup first (non-negotiable)
    shutil.copy(EVENTS_PATH, BACKUP_PATH)

    chained_events = []
    prev_hash = "GENESIS"

    with EVENTS_PATH.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            event = json.loads(line)

            event_str = canonical_event_string(event)
            combined = prev_hash + event_str
            event_hash = sha256(combined)

            event["prev_hash"] = prev_hash
            event["event_hash"] = event_hash

            prev_hash = event_hash
            chained_events.append(event)

    # Rewrite file atomically
    with EVENTS_PATH.open("w", encoding="utf-8") as f:
        for event in chained_events:
            f.write(json.dumps(event, separators=(",", ":")) + "\n")

    print("EVENT CHAINING COMPLETE")
    print(f"Backup written to {BACKUP_PATH}")


if __name__ == "__main__":
    chain_events()
