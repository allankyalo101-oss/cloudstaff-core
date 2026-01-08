# sarah_db_upgrade.py
# Corrected DB upgrade for Day 2+ stress testing
# Permanent storage path: /home/cloudstaff/cloudstaff-core/sarah_db_upgrade.py

import sqlite3

DB_FILE = "sarah.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Step 1: Check existing columns
cursor.execute("PRAGMA table_info(ledger)")
columns = [col[1] for col in cursor.fetchall()]
print("Existing columns:", columns)

# Step 2: Add missing columns without defaults
missing_columns = []
if "type" not in columns:
    cursor.execute("ALTER TABLE ledger ADD COLUMN type TEXT")
    missing_columns.append("type")
if "status" not in columns:
    cursor.execute("ALTER TABLE ledger ADD COLUMN status TEXT")
    missing_columns.append("status")

print("Added columns:", missing_columns)

# Step 3: Fill missing values for existing rows
if "type" in missing_columns:
    cursor.execute("UPDATE ledger SET type = 'Invoice' WHERE type IS NULL")
if "status" in missing_columns:
    cursor.execute("UPDATE ledger SET status = 'pending' WHERE status IS NULL")

conn.commit()
conn.close()
print("Database upgrade complete.")
