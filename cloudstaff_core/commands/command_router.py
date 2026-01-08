from cloudstaff_core.agents.sarah import Sarah

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

    def __init__(self):
        self.sarah = Sarah()

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

        # Ask Sarah for current state (single source of truth)
        last_state = self.sarah.get_last_state(client_name)
        allowed = self.TRANSITION_RULES.get(last_state, [])

        if action not in allowed:
            return f"Illegal action '{action}' from state '{last_state or 'None'}'."

        # Delegate execution to Sarah (Sarah logs to ledger)
        if action == "onboard":
            return self.sarah.client_intake(client_name)
        elif action == "meet":
            return self.sarah.schedule_meeting(client_name)
        elif action == "followup":
            return self.sarah.send_follow_up(client_name)
        elif action == "invoice":
            return self.sarah.record_invoice(client_name, amount)
        elif action == "payment":
            return self.sarah.record_payment(client_name, amount)

        return f"Unknown action '{action}'."
              