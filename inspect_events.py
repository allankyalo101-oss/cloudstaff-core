import json
from pathlib import Path

EVENTS_PATH = Path("cloudstaff_core/storage/events/events.jsonl")

with open(EVENTS_PATH, "r") as f:
    for i, line in enumerate(f, start=1):
        try:
            e = json.loads(line)
            _ = e["client_name"]  # check key
            _ = e["type"]
        except KeyError:
            print(f"Malformed event at line {i}: {line.strip()}")

