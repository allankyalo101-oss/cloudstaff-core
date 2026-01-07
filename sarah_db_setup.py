import sqlite3

# Connect to the SQLite database (will create if it doesn't exist)
conn = sqlite3.connect("sarah.db")
c = conn.cursor()

# Create ledger table if it doesn't exist
c.execute("""
CREATE TABLE IF NOT EXISTS ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT NOT NULL,
    transaction_type TEXT,
    amount REAL,
    date TEXT,
    notes TEXT,
    state TEXT,
    description TEXT
)
""")
conn.commit()
print("✅ Ledger table exists with all necessary columns.")

# Sample entries with client_name included
sample_entries = [
    ("Alice", "Invoice", 250.0, "2026-01-01", "First payment", "pending", "Initial invoice"),
    ("Bob", "Payment", 500.0, "2026-01-02", "Completed payment", "complete", "Second transaction"),
    ("Charlie", "Invoice", 750.0, "2026-01-03", "Follow-up invoice", "pending", "Third transaction")
]

# Insert sample entries
try:
    c.executemany("""
    INSERT INTO ledger (client_name, transaction_type, amount, date, notes, state, description)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_entries)
    conn.commit()
    print("✅ Sample entries inserted successfully.")
except sqlite3.IntegrityError as e:
    print("⚠️ IntegrityError:", e)

# Verify inserted data
c.execute("SELECT * FROM ledger")
rows = c.fetchall()
for row in rows:
    print(row)

# Close connection
conn.close()
