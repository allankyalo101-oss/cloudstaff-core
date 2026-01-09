import sqlite3
from datetime import datetime, timedelta

DB_PATH = "sarah.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

# -----------------------
# Core multi-client operations
# -----------------------
def get_all_clients():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT client_name FROM ledger")
    clients = [row[0] for row in cursor.fetchall()]
    conn.close()
    return clients

def client_report(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Invoice'", (name,))
    total_invoiced = cursor.fetchone()[0] or 0.0
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Payment'", (name,))
    total_paid = cursor.fetchone()[0] or 0.0
    cursor.execute("SELECT COUNT(*) FROM ledger WHERE client_name=? AND type='Invoice'", (name,))
    invoice_count = cursor.fetchone()[0] or 0
    avg_invoice = total_invoiced / invoice_count if invoice_count else 0.0
    balance = total_invoiced - total_paid
    conn.close()
    return {
        "name": name,
        "invoiced": total_invoiced,
        "paid": total_paid,
        "balance": balance,
        "avg_invoice": round(avg_invoice, 2),
        "invoice_count": invoice_count
    }

def overdue_clients(days=30):
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT client_name, SUM(amount) FROM ledger
        WHERE type='Invoice' AND state='pending' AND date <= ?
        GROUP BY client_name
    """, (cutoff,))
    result = cursor.fetchall()
    conn.close()
    return [{"client": r[0], "amount": r[1]} for r in result]

# -----------------------
# Priority alerts
# -----------------------
def high_value_clients(threshold=1000):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT client_name, SUM(amount) FROM ledger
        WHERE type='Invoice'
        GROUP BY client_name
        HAVING SUM(amount) >= ?
    """, (threshold,))
    result = cursor.fetchall()
    conn.close()
    return [{"client": r[0], "total_invoiced": r[1]} for r in result]

# -----------------------
# Semantic search
# -----------------------
def search_clients(keyword):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT client_name, description, type, amount FROM ledger
        WHERE client_name LIKE ? OR description LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))
    result = cursor.fetchall()
    conn.close()
    return result

# -----------------------
# Automated notifications
# -----------------------
def notify_overdue():
    overdue = overdue_clients()
    for entry in overdue:
        print(f"FOLLOW-UP: {entry['client']} has overdue balance of {entry['amount']:.2f}")

def notify_high_value():
    high_value = high_value_clients()
    for entry in high_value:
        print(f"PRIORITY ALERT: {entry['client']} is high-value with total invoiced {entry['total_invoiced']:.2f}")

# -----------------------
# Combined daily notifications
# -----------------------
def daily_notifications():
    notify_overdue()
    notify_high_value()

if __name__ == "__main__":
    print("Day 10 advanced multi-client system loaded.")
    daily_notifications()
