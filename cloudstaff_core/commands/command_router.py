import sqlite3
from cloudstaff_core.agents.sarah import Sarah

DB_PATH = "sarah.db"


class CommandRouter:
    """
    Enforces per-client workflow transitions.
    """

    TRANSITION_RULES = {
        None: ["onboard"],
        "intake_completed": ["meet"],
        "meeting_scheduled": ["followup"],
        "follow_up_sent": ["invoice"],
        "invoice_issued": ["payment"],
        "payment_received": [],
    }

    def __init__(self):
        self.sarah = Sarah()

    def execute(self, command: str):
        parts = command.strip().split()
        if not parts:
            return "Empty command"

        action = parts[0].lower()

        # REPORT IS ALWAYS ALLOWED
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
