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
        "avg_invoice": avg_invoice,
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
# Bulk operations
# -----------------------
def bulk_invoice(clients, amounts, description="Bulk Invoice"):
    conn = connect_db()
    cursor = conn.cursor()
    for name, amt in zip(clients, amounts):
        cursor.execute("INSERT INTO ledger (client_name, transaction_type, amount, date, notes, state, description, type, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (name, "Invoice", amt, datetime.now().strftime("%Y-%m-%d"), "Automated bulk", "pending", description, "Invoice", "open"))
    conn.commit()
    conn.close()

def bulk_payment(clients, amounts):
    conn = connect_db()
    cursor = conn.cursor()
    for name, amt in zip(clients, amounts):
        cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Invoice'", (name,))
        total_invoiced = cursor.fetchone()[0] or 0.0
        cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Payment'", (name,))
        total_paid = cursor.fetchone()[0] or 0.0
        if total_paid + amt > total_invoiced:
            print(f"Payment rejected: balance already settled for {name}.")
            continue
        cursor.execute("INSERT INTO ledger (client_name, transaction_type, amount, date, notes, state, description, type, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (name, "Payment", amt, datetime.now().strftime("%Y-%m-%d"), "Automated bulk", "complete", "Bulk payment", "Payment", "closed"))
    conn.commit()
    conn.close()

# -----------------------
# Automated notifications
# -----------------------
def notify_overdue():
    overdue = overdue_clients()
    for entry in overdue:
        print(f"ALERT: {entry['client']} has overdue balance of {entry['amount']}")

if __name__ == "__main__":
    print("Day 5 advanced multi-client system loaded.")

