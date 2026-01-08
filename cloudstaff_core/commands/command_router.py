# cloudstaff_core/commands/command_router.py
# =========================================
# Command Router – Workflow + Economic Gatekeeper
# Idempotent, Ledger-Validated
# =========================================

from cloudstaff_core.agents.sarah import Sarah
import sqlite3


class CommandRouter:
    """
    Enforces per-client workflow, economic legality,
    and idempotency guarantees.
    """

    TRANSITION_RULES = {
        None: ["onboard"],
        "intake_completed": ["meet"],
        "meeting_scheduled": ["followup"],
        "follow_up_sent": ["invoice"],
        "invoice_issued": ["payment"],
        "payment_received": ["payment"],  # allow partial payments
    }

    def __init__(self):
        self.sarah = Sarah()
        self.conn = self.sarah.conn
        self.conn.row_factory = sqlite3.Row

    # -------------------------------------
    # PUBLIC ENTRY
    # -------------------------------------
    def execute(self, command: str):
        parts = command.strip().split()
        if not parts:
            return "Empty command"

        action = parts[0].lower()

        # REPORT IS ALWAYS ALLOWED (READ-ONLY)
        if action == "report":
            if len(parts) < 2:
                return "Missing client name"
            return self.sarah.report_client(parts[1])

        if len(parts) < 2:
            return "Missing client name"

        client = parts[1]
        amount = float(parts[2]) if len(parts) > 2 else 0.0

        last_state = self.sarah.get_last_state(client)
        allowed = self.TRANSITION_RULES.get(last_state, [])

        if action not in allowed:
            return f"Illegal action '{action}' from state '{last_state}'."

        # IDEMPOTENCY GUARDS
        if self._is_duplicate_action(client, action, amount):
            return f"Ignored duplicate '{action}' for {client}."

        # ROUTE ACTION
        if action == "onboard":
            return self.sarah.client_intake(client)
        if action == "meet":
            return self.sarah.schedule_meeting(client)
        if action == "followup":
            return self.sarah.send_follow_up(client)
        if action == "invoice":
            return self.sarah.record_invoice(client, amount)
        if action == "payment":
            return self.sarah.record_payment(client, amount)

        return f"Unknown action '{action}'."

    # -------------------------------------
    # IDEMPOTENCY LOGIC
    # -------------------------------------
    def _is_duplicate_action(self, client: str, action: str, amount: float) -> bool:
        """
        Prevents duplicate economic or workflow actions
        based on most recent ledger entry.
        """
        c = self.conn.cursor()
        c.execute(
            """
            SELECT transaction_type, amount
            FROM ledger
            WHERE client_name = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (client,),
        )
        row = c.fetchone()
        if not row:
            return False

        last_type = row["transaction_type"].lower()
        last_amount = row["amount"]

        # Duplicate workflow actions
        if action in {"onboard", "meet", "followup"} and last_type == action.upper():
            return True

        # Duplicate invoice (same amount twice)
        if action == "invoice" and last_type == "INVOICE" and last_amount == amount:
            return True

        # Duplicate payment (same amount twice)
        if action == "payment" and last_type == "PAYMENT" and last_amount == amount:
            return True

        return False
