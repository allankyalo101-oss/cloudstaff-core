# cloudstaff_core/agents/sarah.py
# =========================================
# Sarah Agent – Ledger-Driven Administrator
# Domain Authority (Single Source of Truth)
# =========================================

import sqlite3
from datetime import datetime
import os
from typing import Dict, List

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "sarah.db")


class Sarah:
    def __init__(self):
        self.name = "Sarah"
        self.role = "Administrative AI Assistant"

        # SQLite connection
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row

        # In-memory ledger mirror
        self.ledger: List[Dict] = []

        self._load_ledger()

    # -------------------------------------
    # INTERNAL STATE MANAGEMENT
    # -------------------------------------
    def _load_ledger(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM ledger ORDER BY id ASC")
        self.ledger = [dict(r) for r in c.fetchall()]

    def get_last_state(self, client_name: str):
        c = self.conn.cursor()
        c.execute(
            "SELECT state FROM ledger WHERE client_name = ? ORDER BY id DESC LIMIT 1",
            (client_name,),
        )
        row = c.fetchone()
        return row["state"] if row else None

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
        self._load_ledger()

    # -------------------------------------
    # CORE ACTIONS (DOMAIN RULED)
    # -------------------------------------
    def client_intake(self, name: str):
        last_state = self.get_last_state(name)
        if last_state is not None:
            return f"Illegal action 'onboard' from state '{last_state}'."

        self._persist(
            client_name=name,
            transaction_type="INTAKE",
            amount=0.0,
            state="intake_completed",
            description="Client onboarded",
        )
        return f"Client intake completed for {name}."

    def schedule_meeting(self, name: str):
        if self.get_last_state(name) != "intake_completed":
            return f"Illegal action 'meet' from state '{self.get_last_state(name)}'."

        self._persist(
            client_name=name,
            transaction_type="MEETING",
            amount=0.0,
            state="meeting_scheduled",
            description="Meeting scheduled",
        )
        return f"Meeting scheduled for {name}."

    def send_follow_up(self, name: str):
        if self.get_last_state(name) != "meeting_scheduled":
            return f"Illegal action 'followup' from state '{self.get_last_state(name)}'."

        self._persist(
            client_name=name,
            transaction_type="FOLLOW_UP",
            amount=0.0,
            state="follow_up_sent",
            description="Follow-up email sent",
        )
        return f"Follow-up sent to {name}."

    def record_invoice(self, name: str, amount: float):
        if self.get_last_state(name) != "follow_up_sent":
            return f"Illegal action 'invoice' from state '{self.get_last_state(name)}'."

        self._persist(
            client_name=name,
            transaction_type="INVOICE",
            amount=amount,
            state="invoice_issued",
            description="Invoice recorded",
        )
        return f"Invoice of {amount} recorded for {name}."

    def record_payment(self, name: str, amount: float):
        if self.get_last_state(name) != "invoice_issued":
            return f"Illegal action 'payment' from state '{self.get_last_state(name)}'."

        self._persist(
            client_name=name,
            transaction_type="PAYMENT",
            amount=amount,
            state="payment_received",
            description="Payment received",
        )
        return f"Payment of {amount} received from {name}."

    # -------------------------------------
    # REPORTING
    # -------------------------------------
    def report_client(self, name: str):
        rows = [r for r in self.ledger if r["client_name"] == name]
        if not rows:
            return f"No records for {name}."

        total_invoiced = sum(
            r["amount"] for r in rows if r["transaction_type"] == "INVOICE"
        )
        total_paid = sum(
            r["amount"] for r in rows if r["transaction_type"] == "PAYMENT"
        )

        return (
            f"Client Report: {name}\n"
            f"- Invoiced: {total_invoiced}\n"
            f"- Paid: {total_paid}\n"
            f"- Balance: {total_invoiced - total_paid}"
        )

    def report_all(self):
        return f"Ledger contains {len(self.ledger)} total records."
