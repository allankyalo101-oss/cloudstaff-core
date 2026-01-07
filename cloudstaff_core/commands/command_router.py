from cloudstaff_core.agents.sarah import Sarah

class CommandRouter:
    """
    Routes human-issued text commands to valid Sarah actions.
    Enforces allowed operations and prevents illegal state execution.
    """

    def __init__(self):
        self.sarah = Sarah()

    def execute(self, command: str) -> str:
        if not command or not isinstance(command, str):
            return "Invalid command."

        tokens = command.strip().lower().split()

        if len(tokens) < 2:
            return "Command too short."

        action = tokens[0]
        client = tokens[1].capitalize()

        try:
            if action == "onboard":
                return self.sarah.client_intake(client)

            elif action == "meet":
                return self.sarah.schedule_meeting(client)

            elif action == "followup":
                return self.sarah.send_follow_up(client)

            elif action == "invoice":
                if len(tokens) != 3:
                    return "Usage: invoice <client> <amount>"
                amount = float(tokens[2])
                return self.sarah.record_invoice(client, amount)

            elif action == "payment":
                if len(tokens) != 3:
                    return "Usage: payment <client> <amount>"
                amount = float(tokens[2])
                return self.sarah.record_payment(client, amount)

            elif action == "report":
                return self.sarah.report_client(client)

            else:
                return f"Unknown command: {action}"

        except Exception as e:
            return f"Execution error: {str(e)}"
