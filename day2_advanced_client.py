# day2_advanced_client.py
# Day 2: Advanced multi-client ledger operations
# Permanent storage path: /home/cloudstaff/cloudstaff-core/day2_advanced_client.py

import sqlite3
from datetime import datetime, timedelta

DB_PATH = "sarah.db"

# --- Database connection ---
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- Ensure table exists ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT NOT NULL,
    type TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    notes TEXT
)
""")
conn.commit()

# --- Core operations ---
def onboard_client(name: str):
    print(f"Client intake completed for {name}.")

def schedule_meeting(name: str):
    print(f"Meeting scheduled for {name}.")

def send_followup(name: str):
    print(f"Follow-up sent to {name}.")

def invoice_client(name: str, amount: float, description: str = ""):
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Invoice'", (name,))
    total_invoiced = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Payment'", (name,))
    total_paid = cursor.fetchone()[0] or 0
    balance = total_invoiced - total_paid
    if balance > 0:
        # still has unpaid invoice, allow new invoice
        cursor.execute(
            "INSERT INTO ledger (client_name, type, amount, date, description, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, "Invoice", amount, datetime.now().strftime("%Y-%m-%d"), description, "pending", "Day2 invoice")
        )
        conn.commit()
        print(f"Invoice of {amount} recorded for {name}.")
    else:
        # no unpaid invoice, allow new
        cursor.execute(
            "INSERT INTO ledger (client_name, type, amount, date, description, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, "Invoice", amount, datetime.now().strftime("%Y-%m-%d"), description, "pending", "Day2 invoice")
        )
        conn.commit()
        print(f"Invoice of {amount} recorded for {name}.")

def record_payment(name: str, amount: float):
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Invoice'", (name,))
    total_invoiced = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Payment'", (name,))
    total_paid = cursor.fetchone()[0] or 0
    balance = total_invoiced - total_paid
    if balance <= 0:
        print(f"Payment rejected: balance already settled for {name}.")
        return
    pay_amount = min(amount, balance)
    cursor.execute(
        "INSERT INTO ledger (client_name, type, amount, date, description, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, "Payment", pay_amount, datetime.now().strftime("%Y-%m-%d"), "Day2 payment", "complete", "Recorded payment")
    )
    conn.commit()
    print(f"Payment of {pay_amount} received from {name}.")

def client_report(name: str):
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Invoice'", (name,))
    invoiced = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Payment'", (name,))
    paid = cursor.fetchone()[0] or 0
    balance = invoiced - paid
    print(f"Client Report: {name}")
    print(f"- Invoiced: {invoiced}")
    print(f"- Paid: {paid}")
    print(f"- Balance: {balance}")

def overdue_clients(days: int = 30):
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    cursor.execute("SELECT client_name, SUM(amount) as balance FROM ledger WHERE type='Invoice' AND date <= ? GROUP BY client_name", (cutoff_date,))
    results = cursor.fetchall()
    overdue = []
    for client, bal in results:
        cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Payment'", (client,))
        paid = cursor.fetchone()[0] or 0
        if bal - paid > 0:
            overdue.append((client, bal - paid))
    print("Overdue clients (30+ days):")
    for client, bal in overdue:
        print(f"- {client}: {bal}")
    return overdue

# --- Persistent close ---
def close_db():
    conn.close()
