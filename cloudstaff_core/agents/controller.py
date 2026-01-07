from cloudstaff_core.agents.commands import Command
from cloudstaff_core.agents.state_machine import STATE_TRANSITIONS
from cloudstaff_core.agents.sarah import Sarah


class SarahController:
    def __init__(self):
        self.sarah = Sarah()

    def execute(self, command: Command, payload: str = "") -> str:
        current_state = self.sarah.workflow_state
        allowed = STATE_TRANSITIONS.get(current_state, set())

        if command.value not in allowed:
            return (
                f"Illegal action '{command.value}' "
                f"from state '{current_state}'."
            )

        # Dispatch
        if command == Command.STATUS:
            return self.sarah.respond("status")

        if command == Command.REPORT:
            return self.sarah.respond("report")

        if command == Command.RESET:
            return self.sarah.respond("reset")

        if command == Command.CLIENT_INTAKE:
            return self.sarah.respond("client intake")

        if command == Command.SCHEDULE_MEETING:
            text = "schedule meeting"
            if payload:
                text += f" {payload}"
            return self.sarah.respond(text)

        if command == Command.SEND_FOLLOW_UP:
            return self.sarah.respond("send follow up")

        if command == Command.SUMMARIZE:
            return self.sarah.respond(f"summarize {payload}")

        return "Unhandled command."

