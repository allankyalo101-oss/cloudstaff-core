import sqlite3
from datetime import datetime, timedelta

DB_PATH = "sarah.db"

# -----------------------
# Database connection
# -----------------------
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
    balance = total_invoiced - total_paid

    # Aggregate metrics
    cursor.execute("SELECT AVG(amount) FROM ledger WHERE client_name=? AND type='Invoice'", (name,))
    avg_invoice = cursor.fetchone()[0] or 0.0
    cursor.execute("SELECT COUNT(*) FROM ledger WHERE client_name=? AND type='Invoice'", (name,))
    invoice_count = cursor.fetchone()[0] or 0

    conn.close()
    return {
        "name": name,
        "invoiced": total_invoiced,
        "paid": total_paid,
        "balance": balance,
        "avg_invoice": avg_invoice,
        "invoice_count": invoice_count
    }

# -----------------------
# Overdue & priority clients
# -----------------------
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

# -----------------------
# Semantic search
# -----------------------
def search_clients(keyword, types=None):
    types_filter = ""
    params = (f"%{keyword}%", f"%{keyword}%")
    if types:
        types_placeholders = ",".join("?"*len(types))
        types_filter = f" AND type IN ({types_placeholders})"
        params += tuple(types)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT client_name, description, type, amount FROM ledger
        WHERE (client_name LIKE ? OR description LIKE ?){types_filter}
    """, params)
    result = cursor.fetchall()
    conn.close()
    return result

# -----------------------
# Automated notifications & reminders
# -----------------------
def notify_overdue(days=30):
    overdue = overdue_clients(days)
    for entry in overdue:
        print(f"ALERT: {entry['client']} has overdue balance of {entry['amount']}")

def send_payment_reminders():
    overdue = overdue_clients()
    for entry in overdue:
        print(f"REMINDER: Send payment reminder to {entry['client']} for {entry['amount']} due.")

# -----------------------
# Day 4 stress-test helpers
# -----------------------
def record_invoice(name, amount, description=""):
    conn = connect_db()
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO ledger (client_name, transaction_type, amount, date, notes, state, description, type, status)
        VALUES (?, 'Invoice', ?, ?, '', 'pending', ?, 'Invoice', 'pending')
    """, (name, amount, date_str, description))
    conn.commit()
    conn.close()
    print(f"Invoice of {amount} recorded for {name}.")

def record_payment(name, amount):
    conn = connect_db()
    cursor = conn.cursor()
    # Check balance
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Invoice'", (name,))
    total_invoiced = cursor.fetchone()[0] or 0.0
    cursor.execute("SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Payment'", (name,))
    total_paid = cursor.fetchone()[0] or 0.0
    balance = total_invoiced - total_paid
    if amount > balance:
        print(f"Payment rejected: balance already settled for {name}.")
        conn.close()
        return
    date_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO ledger (client_name, transaction_type, amount, date, notes, state, description, type, status)
        VALUES (?, 'Payment', ?, ?, '', 'complete', 'Payment received', 'Payment', 'complete')
    """, (name, amount, date_str))
    conn.commit()
    conn.close()
    print(f"Payment of {amount} received from {name}.")

if __name__ == "__main__":
    print("Day 4 multi-client system loaded.")
    # Optional: auto-run reminders for testing
    send_payment_reminders()
