import re
from datetime import datetime
from typing import List, Dict


class Sarah:
    def __init__(self):
        self.name = "Sarah"
        self.role = "Administrative AI Assistant"

        self.workflow_state = "idle"
        self.memory: List[Dict] = []
        self.ledger: List[Dict] = []

        self.last_client = None
        self.last_meeting = None

        self.system_commands = {"status", "report", "reset"}

    # ------------------------------
    # System Prompt
    # ------------------------------
    def system_prompt(self) -> str:
        return (
            "You are Sarah, a professional administrative assistant AI. "
            "You execute administrative workflows deterministically."
        )

    # ------------------------------
    # Utilities
    # ------------------------------
    def _log(self, action_type: str, details: Dict = None):
        self.ledger.append({
            "timestamp": datetime.utcnow().isoformat(),
            "state": self.workflow_state,
            "type": action_type,
            "details": details or {}
        })

    def _in_scope(self, user_input: str) -> bool:
        keywords = [
            "email", "meeting", "schedule",
            "summarize", "summary",
            "client intake", "intake",
            "follow up", "follow-up",
            "report", "status"
        ]
        return any(k in user_input.lower() for k in keywords)

    # ------------------------------
    # System Commands
    # ------------------------------
    def _handle_status(self) -> str:
        self._log("status_requested")
        return (
            f"System Status:\n"
            f"- State: {self.workflow_state}\n"
            f"- Actions logged: {len(self.ledger)}"
        )

    def _handle_report(self) -> str:
        self._log("report_generated")

        lines = [
            f"Administrative Report – {self.name}",
            "-" * 40,
            f"Current workflow state: {self.workflow_state}",
            "",
            "Recorded actions:"
        ]

        if not self.ledger:
            lines.append("- No actions recorded.")
        else:
            for i, entry in enumerate(self.ledger, start=1):
                lines.append(
                    f"{i}. [{entry['timestamp']}] "
                    f"{entry['type']} | State: {entry['state']}"
                )

        return "\n".join(lines)

    def _handle_reset(self) -> str:
        self.workflow_state = "idle"
        self.memory.clear()
        self.ledger.clear()
        self.last_client = None
        self.last_meeting = None
        return "System reset complete."

    # ------------------------------
    # Workflows
    # ------------------------------
    def handle_client_intake(self) -> str:
        self.workflow_state = "intake_completed"
        self._log("client_intake_completed")

        return (
            "Client intake initiated.\n"
            "Please provide client details."
        )

    def schedule_meeting(self, user_input: str) -> str:
        self.workflow_state = "meeting_scheduled"
        self._log("meeting_scheduled")

        return "Meeting scheduled."

    def send_follow_up(self) -> str:
        if self.workflow_state != "meeting_scheduled":
            return "No meeting available for follow-up."

        self.workflow_state = "follow_up_sent"
        self._log("follow_up_sent")

        return "Follow-up sent."

    def summarize_text(self, text: str) -> str:
        self._log("summary_generated")
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return "\n".join(f"- {s}" for s in sentences if s)

    # ------------------------------
    # Router
    # ------------------------------
    def respond(self, user_input: str) -> str:
        clean = user_input.strip().lower()

        if clean in self.system_commands:
            if clean == "status":
                response = self._handle_status()
            elif clean == "report":
                response = self._handle_report()
            elif clean == "reset":
                response = self._handle_reset()

        elif not self._in_scope(user_input):
            response = "Out of scope."

        elif "intake" in clean:
            response = self.handle_client_intake()

        elif "schedule" in clean or "meeting" in clean:
            response = self.schedule_meeting(user_input)

        elif "follow up" in clean or "email" in clean:
            response = self.send_follow_up()

        elif "summarize" in clean:
            response = self.summarize_text(user_input)

        else:
            response = "Administrative request acknowledged."

        self.memory.append({
            "user": user_input,
            "sarah": response
        })

        return response
