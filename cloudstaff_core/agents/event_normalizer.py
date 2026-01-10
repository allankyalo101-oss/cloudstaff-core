import json
from pathlib import Path
from datetime import datetime

EVENTS_PATH = Path("cloudstaff_core/storage/events/events.jsonl")
BACKUP_PATH = Path("cloudstaff_core/storage/events/events.backup.jsonl")

ALLOWED_ACTIONS = {
    "Invoice issued": "INVOICE",
    "Payment received": "PAYMENT",
}

def normalize_event(raw):
    if "client_name" in raw:
        return raw  # already canonical

    action = raw.get("action")
    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"Unknown action: {action}")

    return {
        "timestamp": raw.get("timestamp", datetime.utcnow().isoformat()),
        "client_name": raw["client"],
        "event_type": ALLOWED_ACTIONS[action],
        "amount": float(raw["amount"]),
        "source": "normalized_migration"
    }

def normalize_events():
    if not EVENTS_PATH.exists():
        raise FileNotFoundError("events.jsonl not found")

    raw_lines = EVENTS_PATH.read_text().splitlines()
    normalized = []

    for idx, line in enumerate(raw_lines, start=1):
        try:
            raw = json.loads(line)
            normalized.append(normalize_event(raw))
        except Exception as e:
            raise RuntimeError(f"Failed at line {idx}: {e}")

    BACKUP_PATH.write_text("\n".join(raw_lines) + "\n")
    EVENTS_PATH.write_text("\n".join(json.dumps(e) for e in normalized) + "\n")

    print("EVENT NORMALIZATION COMPLETE")
    print(f"Backup written to {BACKUP_PATH}")

if __name__ == "__main__":
    normalize_events()
