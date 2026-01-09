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

    cursor.execute(
        "SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Invoice'",
        (name,),
    )
    total_invoiced = cursor.fetchone()[0] or 0.0

    cursor.execute(
        "SELECT SUM(amount) FROM ledger WHERE client_name=? AND type='Payment'",
        (name,),
    )
    total_paid = cursor.fetchone()[0] or 0.0

    conn.close()

    return {
        "name": name,
        "invoiced": total_invoiced,
        "paid": total_paid,
        "balance": total_invoiced - total_paid,
    }


def overdue_clients(days=30):
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT client_name, SUM(amount)
        FROM ledger
        WHERE type='Invoice'
          AND state='pending'
          AND amount > 0
          AND date <= ?
        GROUP BY client_name
        """,
        (cutoff,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [{"client": r[0], "amount": r[1]} for r in rows]


# -----------------------
# Priority alerts
# -----------------------
def high_value_clients(threshold=1000):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT client_name, SUM(amount)
        FROM ledger
        WHERE type='Invoice'
          AND amount > 0
        GROUP BY client_name
        HAVING SUM(amount) >= ?
        """,
        (threshold,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [{"client": r[0], "total_invoiced": r[1]} for r in rows]


# -----------------------
# Semantic search (HARDENED)
# -----------------------
def search_clients(keyword):
    """
    Semantic search across meaningful records only.
    Excludes zero-amount operational noise.
    """

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT client_name, description, type, amount
        FROM ledger
        WHERE (client_name LIKE ? OR description LIKE ?)
          AND NOT (amount = 0 AND type IN ('Invoice', 'Payment'))
        ORDER BY date DESC
        """,
        (f"%{keyword}%", f"%{keyword}%"),
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


# -----------------------
# Automated notifications
# -----------------------
def notify_overdue():
    for entry in overdue_clients():
        print(
            f"ALERT: {entry['client']} has overdue balance of {entry['amount']}"
        )


if __name__ == "__main__":
    print("Day 3 advanced client analytics loaded.")
