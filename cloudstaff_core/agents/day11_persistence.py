import json
from pathlib import Path
from cloudstaff_core.agents.event_replay import replay_events

SNAPSHOT_PATH = Path("cloudstaff_core/storage/snapshots/latest.json")


def write_snapshot():
    state = replay_events()
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with SNAPSHOT_PATH.open("w", encoding="utf-8") as f:
        json.dump(state, f, sort_keys=True, indent=2)

    print("Snapshot written. Events persisted.")


if __name__ == "__main__":
    write_snapshot()
