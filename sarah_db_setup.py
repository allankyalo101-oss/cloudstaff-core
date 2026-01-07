import sqlite3

# Connect to your existing database
conn = sqlite3.connect("cloudstaff_sarah.db")
c = conn.cursor()

# Add 'state' column to existing ledger table if it doesn't exist
c.execute("""
    ALTER TABLE ledger
    ADD COLUMN state TEXT DEFAULT 'unknown';
""")

# Optional: Verify schema update
c.execute("PRAGMA table_info(ledger);")
columns = c.fetchall()
print("Updated ledger table schema:")
for col in columns:
    print(col)

conn.commit()
conn.close()
