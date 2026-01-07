import sqlite3
from cloudstaff_core.agents.sarah import Sarah

DB_PATH = "sarah.db"

class CommandRouter:
    """
    Routes structured commands to Sarah, enforcing allowed state transitions.
    """

    # Define allowed actions based on last state
    TRANSITION_RULES = {
        None: ["onboard"],                  # No previous record → only onboarding allowed
        "intake_completed": ["meet"],
        "meeting_scheduled": ["followup"],
        "follow_up_sent": ["invoice"],
        "invoice_issued": ["payment"],
        "payment_received": [],             # Completed cycle
    }

    STATE_MAPPING = {
        "onboard": "intake_completed",
        "meet": "meeting_scheduled",
        "followup": "follow_up_sent",
        "invoice": "invoice_issued",
        "payment": "payment_received",
    }

    def __init__(self):
        self.sarah = Sarah()
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def execute(self, command: str):
        """
        Executes a structured command (e.g., 'onboard Alice', 'invoice Bob 500')
        """

        parts = command.strip().split()
        if not parts:
            return "Empty command"

        action = parts[0].lower()
        if len(parts) < 2:
            return "Missing client name"

        client_name = parts[1]
        amount = float(parts[2]) if len(parts) > 2 else 0.0

        last_state = self._get_last_state(client_name)
        allowed = self.TRANSITION_RULES.get(last_state, [])

        if action not in allowed:
            return f"Illegal action '{action}' from state '{last_state or 'None'}'."

        # Route action to Sarah
        if action == "onboard":
            result = self.sarah.client_intake(client_name)
        elif action == "meet":
            result = self.sarah.schedule_meeting(client_name)
        elif action == "followup":
            result = self.sarah.send_follow_up(client_name)
        elif action == "invoice":
            result = self.sarah.record_invoice(client_name, amount)
        elif action == "payment":
            result = self.sarah.record_payment(client_name, amount)
        else:
            return f"Unknown action '{action}'."

        # Log action in ledger
        self._log_action(client_name, action, amount)

        return result

    def _get_last_state(self, client_name: str):
        """
        Retrieves the latest state for a client from ledger
        """
        self.c.execute(
            "SELECT state FROM ledger WHERE client_name = ? ORDER BY id DESC LIMIT 1",
            (client_name,),
        )
        row = self.c.fetchone()
        return row["state"] if row else None

    def _log_action(self, client_name: str, action: str, amount: float):
        """
        Inserts a ledger record for the performed action
        """
        state = self.STATE_MAPPING.get(action, "unknown")
        description = f"{action} performed"
        self.c.execute(
            "INSERT INTO ledger (client_name, transaction_type, amount, state, description) VALUES (?, ?, ?, ?, ?)",
            (client_name, action.upper(), amount, state, description),
        )
        self.conn.commit()
