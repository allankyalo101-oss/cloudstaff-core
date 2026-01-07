import sqlite3

# Connect to the database
conn = sqlite3.connect("sarah.db")
c = conn.cursor()

# Add 'description' column if it does not exist
try:
    c.execute("ALTER TABLE ledger ADD COLUMN description TEXT")
    print("✅ 'description' column added to 'ledger'")
except sqlite3.OperationalError:
    print("ℹ 'description' column already exists")

# Sample entries to insert
sample_entries = [
    ("pending", "Order from Alice - 2 items"),
    ("completed", "Order from Bob - 1 item"),
    ("pending", "Order from Charlie - 5 items")
]

# Insert sample entries into the ledger
c.executemany("INSERT INTO ledger (state, description) VALUES (?, ?)", sample_entries)
conn.commit()
print("✅ Sample ledger entries inserted successfully.")

# Verify current table state
c.execute("SELECT * FROM ledger")
rows = c.fetchall()
print("Current ledger table contents:")
for row in rows:
    print(row)

# Close the connection
conn.close()
