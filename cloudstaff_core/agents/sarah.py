# ==============================
# Sarah Agent – Administrative Workflow Assistant
# Day 1 – Execution Locked
# ==============================

import re
from datetime import datetime
from typing import List, Dict


class Sarah:
    # ------------------------------
    # Initialization
    # ------------------------------
    def __init__(self):
        self.name = "Sarah"
        self.role = "Administrative AI Assistant"

        # Explicit workflow state
        self.workflow_state = "idle"

        # Session memory (non-authoritative)
        self.memory: List[Dict] = []

        # Append-only administrative ledger
        self.ledger: List[Dict] = []

        # Last known entities
        self.last_client = None
        self.last_meeting = None

        # System commands
        self.system_commands = {"status", "report", "reset"}

    # ------------------------------
    # System Prompt
    # ------------------------------
    def system_prompt(self) -> str:
        return (
            "You are Sarah, a professional administrative assistant AI. "
            "You execute administrative workflows deterministically, "
            "log actions, and report accurately. "
            "You do not request clarification when execution is possible."
        )

    # ------------------------------
    # Internal Utilities
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
    # System Command Handlers
    # ------------------------------
    def _handle_status(self) -> str:
        self._log("status_requested")
        return (
            f"System Status:\n"
            f"- Current state: {self.workflow_state}\n"
            f"- Logged actions: {len(self.ledger)}"
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

        lines.append("")
        lines.append("Next expected step:")

        if self.workflow_state == "intake_completed":
            lines.append("- Schedule a meeting.")
        elif self.workflow_state == "meeting_scheduled":
            lines.append("- Send a follow-up email.")
        elif self.workflow_state == "follow_up_sent":
            lines.append("- Await further administrative instruction.")
        else:
            lines.append("- Await administrative task.")

        return "\n".join(lines)

    def _handle_reset(self) -> str:
        self.workflow_state = "idle"
        self.memory.clear()
        self.ledger.clear()
        self.last_client = None
        self.last_meeting = None
        return "System reset complete. Workflow and records cleared."

    # ------------------------------
    # Client Intake
    # ------------------------------
    def handle_client_intake(self) -> str:
        self.workflow_state = "intake_completed"
        self._log("client_intake_completed")

        return (
            "Client intake initiated.\n\n"
            "Please provide:\n"
            "1. Full Name\n"
            "2. Company Name\n"
            "3. Email Address\n"
            "4. Phone Number\n"
            "5. Nature of Inquiry\n\n"
            "Once received, a meeting can be scheduled."
        )

    # ------------------------------
    # Meeting Scheduler (Deterministic)
    # ------------------------------
    def schedule_meeting(self, user_input: str) -> str:
        date = "Friday"
        time = "10:00 AM"

        date_match = re.search(r'on ([\w\s\d]+)', user_input, re.IGNORECASE)
        time_match = re.search(
            r'at (\d{1,2}(:\d{2})?\s?(AM|PM)?)',
            user_input,
            re.IGNORECASE
        )

        if date_match:
            date = date_match.group(1).strip()
        if time_match:
            time = time_match.group(1).strip()

        meeting = {
            "date": date,
            "time": time
        }

        self.last_meeting = meeting
        self.workflow_state = "meeting_scheduled"
        self._log("meeting_scheduled", meeting)

        return (
            f"Meeting successfully scheduled on {date} at {time}.\n"
            "You may request a follow-up when appropriate."
        )

    # ------------------------------
    # Follow-Up Email
    # ------------------------------
    def send_follow_up(self) -> str:
        if self.workflow_state != "meeting_scheduled":
            return "No scheduled meeting available for follow-up."

        self.workflow_state = "follow_up_sent"
        self._log("follow_up_sent")

        return (
            "Subject: Thank You for the Meeting\n\n"
            "Dear [Client Name],\n\n"
            "Thank you for taking the time to meet.\n"
            "Please let me know if you require any additional information.\n\n"
            "Best regards,\n"
            f"{self.name}"
        )

    # ------------------------------
    # Summarization
    # ------------------------------
    def summarize_text(self, text: str) -> str:
        self._log("summary_generated")
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return "\n".join(f"- {s}" for s in sentences if s)

    # ------------------------------
    # Main Response Handler
    # ------------------------------
    def respond(self, user_input: str) -> str:
        clean = user_input.strip().lower()

        # ---- System Commands ----
        if clean in self.system_commands:
            if clean == "status":
                response = self._handle_status()
            elif clean == "report":
                response = self._handle_report()
            elif clean == "reset":
                response = self._handle_reset()

        else:
            # ---- Scope Enforcement ----
            if not self._in_scope(user_input):
                response = (
                    "I'm here strictly for administrative support. "
                    "I cannot assist with that request."
                )

            # ---- Deterministic Routing ----
            elif "client intake" in clean or clean == "intake":
                response = self.handle_client_intake()

            elif "schedule" in clean or "meeting" in clean:
                response = self.schedule_meeting(user_input)

            elif "follow up" in clean or "follow-up" in clean or "email" in clean:
                response = self.send_follow_up()

            elif "summarize" in clean or "summary" in clean:
                content = re.sub(r'summarize|summary', '', user_input, flags=re.I).strip()
                response = self.summarize_text(content)

            else:
                response = "Administrative request acknowledged."

        # ---- Session Memory (Non-authoritative) ----
        self.memory.append({
            "user": user_input,
            "sarah": response
        })

        return response


# ==============================
# End of Sarah Agent – Day 1
# ==============================
