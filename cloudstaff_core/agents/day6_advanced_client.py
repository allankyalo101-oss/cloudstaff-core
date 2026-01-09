# File: cloudstaff-core/agents/day6_advanced_client.py

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
    # Total invoiced and paid
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Invoice'", (name,))
    total_invoiced = cursor.fetchone()[0] or 0.0
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Payment'", (name,))
    total_paid = cursor.fetchone()[0] or 0.0
    balance = total_invoiced - total_paid
    # Avg invoice and payment completion %
    cursor.execute("SELECT COUNT(*) FROM ledger WHERE client_name=? AND type='Invoice'", (name,))
    invoice_count = cursor.fetchone()[0] or 0
    avg_invoice = (total_invoiced / invoice_count) if invoice_count else 0.0
    payment_pct = (total_paid / total_invoiced * 100.0) if total_invoiced else 0.0
    conn.close()
    return {
        "name": name,
        "invoiced": total_invoiced,
        "paid": total_paid,
        "balance": balance,
        "avg_invoice": avg_invoice,
        "invoice_count": invoice_count,
        "payment_pct": payment_pct
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
# Automated follow-ups and reminders
# -----------------------
def notify_overdue():
    overdue = overdue_clients()
    for entry in overdue:
        print(f"ALERT: {entry['client']} has overdue balance of {entry['amount']}")

def automated_followups():
    clients = get_all_clients()
    for client in clients:
        report = client_report(client)
        if report["balance"] > 0:
            print(f"FOLLOW-UP: {client} has outstanding balance {report['balance']:.2f} ({report['payment_pct']:.1f}% paid)")
        if report["invoiced"] >= 1000:
            print(f"PRIORITY ALERT: {client} is high-value with total invoiced {report['invoiced']:.2f}")

# -----------------------
# Entry point for testing
# -----------------------
if __name__ == "__main__":
    print("Day 6 advanced client system loaded.")
    automated_followups()
