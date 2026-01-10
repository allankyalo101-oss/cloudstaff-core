import json
import hashlib
from pathlib import Path
from datetime import datetime
from cloudstaff-core.agents.event_replay import replay_events

BASE_DIR = Path(__file__).resolve().parents[2]
SNAPSHOT_DIR = BASE_DIR / "cloudstaff_core" / "storage" / "snapshots"
SNAPSHOT_PATH = SNAPSHOT_DIR / "latest.json"

SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def hash_state(state: dict) -> str:
    canonical = json.dumps(state, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


def write_snapshot():
    state = replay_events()

    snapshot = {
        "generated_at": datetime.utcnow().isoformat(),
        "state": state,
        "hash": hash_state(state)
    }

    with open(SNAPSHOT_PATH, "w") as f:
        json.dump(snapshot, f, indent=2)

    print("Snapshot written. Events persisted.")


if __name__ == "__main__":
    write_snapshot()
