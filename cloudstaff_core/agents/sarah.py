# cloudstaff_core/agents/sarah.py
# =========================================
# Sarah Agent – Ledger-Driven Administrator
# Day 4 – Economic Authority Locked
# =========================================

import re
import sqlite3
import json
from datetime import datetime
import os
from typing import Dict, List

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "sarah.db")


class Sarah:
    def __init__(self):
        self.name = "Sarah"
        self.role = "Administrative AI Assistant"

        # Workflow state
        self.workflow_state = "idle"

        # Audit ledger (in-memory mirror)
        self.ledger: List[Dict] = []

        # SQLite connection
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row

        self._load_state()

    # -------------------------------------
    # DATABASE STATE
    # -------------------------------------
    def _load_state(self):
        c = self.conn.cursor()

        # Load last workflow state
        c.execute(
            "SELECT state FROM ledger ORDER BY id DESC LIMIT 1"
        )
        row = c.fetchone()
        if row and row["state"]:
            self.workflow_state = row["state"]

        # Load ledger mirror
        c.execute("SELECT * FROM ledger ORDER BY id ASC")
        self.ledger = [dict(r) for r in c.fetchall()]

    def _persist(
        self,
        client_name: str,
        transaction_type: str,
        amount: float,
        state: str,
        description: str,
        notes: str = ""
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
                description
            )
        )
        self.conn.commit()
        self.workflow_state = state
        self._load_state()

    # -------------------------------------
    # CORE ACTIONS
    # -------------------------------------
    def client_intake(self, name: str):
        self._persist(
            client_name=name,
            transaction_type="INTAKE",
            amount=0.0,
            state="intake_completed",
            description="Client onboarded"
        )
        return f"Client intake completed for {name}."

    def schedule_meeting(self, name: str):
        if self.workflow_state != "intake_completed":
            return f"Illegal action 'schedule_meeting' from state '{self.workflow_state}'."

        self._persist(
            client_name=name,
            transaction_type="MEETING",
            amount=0.0,
            state="meeting_scheduled",
            description="Meeting scheduled"
        )
        return f"Meeting scheduled for {name}."

    def send_follow_up(self, name: str):
        if self.workflow_state != "meeting_scheduled":
            return f"Illegal action 'send_follow_up' from state '{self.workflow_state}'."

        self._persist(
            client_name=name,
            transaction_type="FOLLOW_UP",
            amount=0.0,
            state="follow_up_sent",
            description="Follow-up email sent"
        )
        return f"Follow-up sent to {name}."

    def record_invoice(self, name: str, amount: float):
        self._persist(
            client_name=name,
            transaction_type="INVOICE",
            amount=amount,
            state="invoice_issued",
            description="Invoice recorded"
        )
        return f"Invoice of {amount} recorded for {name}."

    def record_payment(self, name: str, amount: float):
        if not any(
            r["client_name"] == name and r["transaction_type"] == "INVOICE"
            for r in self.ledger
        ):
            return "Payment rejected: no invoice exists."

        self._persist(
            client_name=name,
            transaction_type="PAYMENT",
            amount=amount,
            state="payment_received",
            description="Payment received"
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
