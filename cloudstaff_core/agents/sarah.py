# cloudstaff_core/agents/sarah.py
# =========================================
# Sarah Agent – Ledger-Driven Economic Authority
# Stateless, Per-Client Intelligence
# =========================================

import sqlite3
from datetime import datetime
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "sarah.db")


class Sarah:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row

    # -------------------------------------
    # STATE & FINANCIAL READ (READ-ONLY)
    # -------------------------------------
    def get_last_state(self, client_name: str):
        c = self.conn.cursor()
        c.execute(
            "SELECT state FROM ledger WHERE client_name = ? ORDER BY id DESC LIMIT 1",
            (client_name,),
        )
        row = c.fetchone()
        return row["state"] if row else None

    def get_financials(self, client_name: str):
        c = self.conn.cursor()
        c.execute(
            "SELECT transaction_type, amount FROM ledger WHERE client_name = ?",
            (client_name,),
        )
        rows = c.fetchall()

        invoiced = sum(
            r["amount"] for r in rows if r["transaction_type"] == "INVOICE"
        )
        paid = sum(
            r["amount"] for r in rows if r["transaction_type"] == "PAYMENT"
        )

        return {
            "invoiced": invoiced,
            "paid": paid,
            "balance": invoiced - paid,
        }

    # -------------------------------------
    # LEDGER WRITE (AUTHORITATIVE)
    # -------------------------------------
    def _persist(
        self,
        client_name: str,
        transaction_type: str,
        amount: float,
        state: str,
        description: str,
        notes: str = "",
    ):
        c = self.conn.cursor()
        c.execute(
            """
            INSERT INTO ledger
            (client_name, transaction_type, amount, date, notes, state, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                client_name,
                transaction_type,
                amount,
                datetime.utcnow().isoformat(),
                notes,
                state,
                description,
            ),
        )
        self.conn.commit()

    # -------------------------------------
    # ACTIONS (NO WORKFLOW ENFORCEMENT)
    # -------------------------------------
    def client_intake(self, name: str):
        self._persist(name, "INTAKE", 0.0, "intake_completed", "Client onboarded")
        return f"Client intake completed for {name}."

    def schedule_meeting(self, name: str):
        self._persist(name, "MEETING", 0.0, "meeting_scheduled", "Meeting scheduled")
        return f"Meeting scheduled for {name}."

    def send_follow_up(self, name: str):
        self._persist(name, "FOLLOW_UP", 0.0, "follow_up_sent", "Follow-up email sent")
        return f"Follow-up sent to {name}."

    def record_invoice(self, name: str, amount: float):
        self._persist(name, "INVOICE", amount, "invoice_issued", "Invoice recorded")
        return f"Invoice of {amount} recorded for {name}."

    def record_payment(self, name: str, amount: float):
        financials = self.get_financials(name)

        if amount <= 0:
            return "Payment rejected: amount must be positive."

        if financials["balance"] <= 0:
            return "Payment rejected: no outstanding balance."

        if amount > financials["balance"]:
            return (
                f"Payment rejected: amount exceeds balance "
                f"({financials['balance']})."
            )

        self._persist(name, "PAYMENT", amount, "payment_received", "Payment received")
        return f"Payment of {amount} received from {name}."

    # -------------------------------------
    # REPORTING
    # -------------------------------------
    def report_client(self, name: str):
        f = self.get_financials(name)

        if f["invoiced"] == 0 and f["paid"] == 0:
            return f"No records for {name}."

        return (
            f"Client Report: {name}\n"
            f"- Invoiced: {f['invoiced']}\n"
            f"- Paid: {f['paid']}\n"
            f"- Balance: {f['balance']}"
        )
