import sqlite3

# Connect to the database
conn = sqlite3.connect("sarah.db")
c = conn.cursor()

# Create 'ledger' table if it doesn't exist, with 'state' and 'description' columns
c.execute("""
CREATE TABLE IF NOT EXISTS ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT,
    description TEXT
)
""")

conn.commit()
print("✅ Database setup complete. 'ledger' table exists with 'state' and 'description' columns.")

# Insert sample ledger entries
sample_entries = [
    ("pending", "Order from Alice - 2 items"),
    ("completed", "Order from Bob - 1 item"),
    ("pending", "Order from Charlie - 5 items")
]

c.executemany("INSERT INTO ledger (state, description) VALUES (?, ?)", sample_entries)
conn.commit()
print("✅ Sample ledger entries inserted successfully.")

conn.close()
