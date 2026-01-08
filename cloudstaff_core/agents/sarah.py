# cloudstaff_core/agents/sarah.py
# =========================================
# Sarah Agent – Ledger-Driven Executor
# Stateless, Per-Client Authority
# =========================================

import sqlite3
from datetime import datetime
import os
from typing import Dict, List

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "sarah.db")


class Sarah:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row

    # -------------------------------------
    # STATE ACCESS (READ-ONLY)
    # -------------------------------------
    def get_last_state(self, client_name: str):
        c = self.conn.cursor()
        c.execute(
            "SELECT state FROM ledger WHERE client_name = ? ORDER BY id DESC LIMIT 1",
            (client_name,),
        )
        row = c.fetchone()
        return row["state"] if row else None

    # -------------------------------------
    # LEDGER WRITE
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
    # ACTIONS (NO STATE ENFORCEMENT)
    # -------------------------------------
    def client_intake(self, name: str):
        self._persist(
            name, "INTAKE", 0.0, "intake_completed", "Client onboarded"
        )
        return f"Client intake completed for {name}."

    def schedule_meeting(self, name: str):
        self._persist(
            name, "MEETING", 0.0, "meeting_scheduled", "Meeting scheduled"
        )
        return f"Meeting scheduled for {name}."

    def send_follow_up(self, name: str):
        self._persist(
            name, "FOLLOW_UP", 0.0, "follow_up_sent", "Follow-up email sent"
        )
        return f"Follow-up sent to {name}."

    def record_invoice(self, name: str, amount: float):
        self._persist(
            name, "INVOICE", amount, "invoice_issued", "Invoice recorded"
        )
        return f"Invoice of {amount} recorded for {name}."

    def record_payment(self, name: str, amount: float):
        self._persist(
            name, "PAYMENT", amount, "payment_received", "Payment received"
        )
        return f"Payment of {amount} received from {name}."

    # -------------------------------------
    # REPORTING (READ-ONLY)
    # -------------------------------------
    def report_client(self, name: str):
        c = self.conn.cursor()
        c.execute(
            "SELECT transaction_type, amount FROM ledger WHERE client_name = ?",
            (name,),
        )
        rows = c.fetchall()

        if not rows:
            return f"No records for {name}."

        invoiced = sum(
            r["amount"] for r in rows if r["transaction_type"] == "INVOICE"
        )
        paid = sum(
            r["amount"] for r in rows if r["transaction_type"] == "PAYMENT"
        )

        return (
            f"Client Report: {name}\n"
            f"- Invoiced: {invoiced}\n"
            f"- Paid: {paid}\n"
            f"- Balance: {invoiced - paid}"
        )
