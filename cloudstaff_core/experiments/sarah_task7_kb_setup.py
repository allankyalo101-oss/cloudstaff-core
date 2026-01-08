import sqlite3
from datetime import datetime
import os

# Ensure the data directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), '../data'), exist_ok=True)
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/sarah_kb.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create KB table
c.execute('''
CREATE TABLE IF NOT EXISTS kb_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client TEXT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    tags TEXT,
    created_at TEXT NOT NULL
)
''')

# Sample entries
entries = [
    ('Noah', 'How do I pay my invoice?', 
     'You can pay your invoice via bank transfer or MPESA. Include the invoice number.', 
     'payment,invoice,how-to', datetime.now().isoformat()),
    ('Olivia', 'What is the refund policy?', 
     'Refunds are processed within 5 business days after approval.', 
     'refund,policy', datetime.now().isoformat()),
    (None, 'How do I schedule a meeting?', 
     'Use the command "meet <client>" to schedule a meeting with a client.', 
     'meeting,schedule,how-to', datetime.now().isoformat())
]

c.executemany('INSERT INTO kb_entries (client, question, answer, tags, created_at) VALUES (?, ?, ?, ?, ?)', entries)

conn.commit()
conn.close()
print("✅ Knowledge base initialized with sample entries at:", DB_PATH)
