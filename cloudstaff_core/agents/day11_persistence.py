import json
from pathlib import Path
from cloudstaff_core.agents.event_replay import replay_events

SNAPSHOT_DIR = Path("cloudstaff_core/storage/snapshots")
SNAPSHOT_PATH = SNAPSHOT_DIR / "latest.json"

def write_snapshot():
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    state = replay_events()

    SNAPSHOT_PATH.write_text(
        json.dumps(state, sort_keys=True, indent=2)
    )

    print("Snapshot written. Events persisted.")

if __name__ == "__main__":
    write_snapshot()
