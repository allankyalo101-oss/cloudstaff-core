import sqlite3

# Connect to the database (creates file if it doesn't exist)
conn = sqlite3.connect("sarah.db")
c = conn.cursor()

# Step 1: Create ledger table if it doesn't exist
c.execute("""
CREATE TABLE IF NOT EXISTS ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT NOT NULL,
    transaction_type TEXT,
    amount REAL,
    date TEXT,
    notes TEXT
)
""")

# Step 2: (Optional) Add 'state' column if not already present
# SQLite doesn't allow IF NOT EXISTS for columns, so we check manually
c.execute("PRAGMA table_info(ledger)")
columns = [col[1] for col in c.fetchall()]
if 'state' not in columns:
    c.execute("ALTER TABLE ledger ADD COLUMN state TEXT")

# Commit changes
conn.commit()
conn.close()

print("✅ Database setup complete. 'ledger' table exists with 'state' column.")
