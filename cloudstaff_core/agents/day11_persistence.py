import os
import json
import sqlite3
from datetime import datetime

BASE_DIR = "cloudstaff_core/storage"
SNAPSHOT_DIR = os.path.join(BASE_DIR, "snapshots")
EVENTS_DIR = os.path.join(BASE_DIR, "events")

SNAPSHOT_PATH = os.path.join(SNAPSHOT_DIR, "latest.json")
EVENTS_PATH = os.path.join(EVENTS_DIR, "events.jsonl")

DB_PATH = "sarah.db"


def ensure_dirs():
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    os.makedirs(EVENTS_DIR, exist_ok=True)


def connect_db():
    return sqlite3.connect(DB_PATH)


def compute_state():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT client_name,
               SUM(CASE WHEN type='Invoice' THEN amount ELSE 0 END) AS invoiced,
               SUM(CASE WHEN type='Payment' THEN amount ELSE 0 END) AS paid
        FROM ledger
        GROUP BY client_name
    """)

    state = {}
    for name, invoiced, paid in cursor.fetchall():
        invoiced = invoiced or 0.0
        paid = paid or 0.0
        state[name] = {
            "invoiced": invoiced,
            "paid": paid,
            "balance": invoiced - paid
        }

    conn.close()
    return state


def write_snapshot():
    ensure_dirs()
    state = compute_state()

    snapshot = {
        "generated_at": datetime.utcnow().isoformat(),
        "state": state
    }

    with open(SNAPSHOT_PATH, "w") as f:
        json.dump(snapshot, f, indent=2)

    print("Snapshot written. Events persisted.")


if __name__ == "__main__":
    write_snapshot()
