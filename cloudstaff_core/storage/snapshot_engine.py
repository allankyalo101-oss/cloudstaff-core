import json
import os
from datetime import date

BASE_DIR = os.path.dirname(__file__)
SNAPSHOT_DIR = os.path.join(BASE_DIR, "snapshots")

os.makedirs(SNAPSHOT_DIR, exist_ok=True)

def save_snapshot(state):
    filename = f"snapshot_{date.today().isoformat()}.json"
    path = os.path.join(SNAPSHOT_DIR, filename)
    with open(path, "w") as f:
        json.dump(state, f, indent=2)

def load_latest_snapshot():
    files = sorted(
        [f for f in os.listdir(SNAPSHOT_DIR) if f.startswith("snapshot_")],
        reverse=True
    )
    if not files:
        return {}
    with open(os.path.join(SNAPSHOT_DIR, files[0]), "r") as f:
        return json.load(f)
