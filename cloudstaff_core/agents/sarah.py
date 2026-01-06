# ==============================
# Sarah Agent – Administrative Workflow Assistant
# ==============================

import re
from typing import List, Dict

class Sarah:
    # ------------------------------
    # Initialization
    # ------------------------------
    def __init__(self):
        self.name = "Sarah"
        self.role = "Administrative AI Assistant"

        self.scope = [
            "email drafting",
            "calendar scheduling",
            "document summarization",
            "client intake",
            "administrative follow-up",
            "administrative reporting"
        ]

        self.memory: List[Dict] = []
        self.ledger: List[Dict] = []

        self.last_client = None
        self.last_meeting = None
        self.workflow_state = "idle"

    # ------------------------------
    # System Prompt
    # ------------------------------
    def system_prompt(self):
        return (
            "You are Sarah, a professional administrative assistant AI. "
            "You operate strictly within administrative support. "
            "You track, log, and report tasks accurately."
        )

    # ------------------------------
    # Scope Checker
    # ------------------------------
    def is_in_scope(self, user_input: str) -> bool:
        keywords = [
            "email", "meeting", "schedule",
            "summarize", "client intake",
            "follow up", "report", "status"
        ]
        return any(k in user_input.lower() for k in keywords)

    # ------------------------------
    # Client Intake
    # ------------------------------
    def handle_client_intake(self) -> str:
        self.workflow_state = "intake_completed"

        self.ledger.append({
            "type": "client_intake",
            "status": "completed"
        })

        return (
            "Client intake initiated.\n\n"
            "Please provide:\n"
            "1. Full Name\n"
            "2. Company Name\n"
            "3. Email Address\n"
            "4. Phone Number\n"
            "5. Nature of Inquiry\n\n"
            "Once received, I can assist with scheduling a meeting."
        )

    # ------------------------------
    # Meeting Scheduler
    # ------------------------------
    def schedule_meeting(self, user_input: str) -> str:
        date = "[Date]"
        time = "[Time]"

        date_match = re.search(r'on ([\w\s\d]+)', user_input, re.IGNORECASE)
        time_match = re.search(r'at (\d{1,2}:\d{2}\s?(AM|PM)?)', user_input, re.IGNORECASE)

        if date_match:
            date = date_match.group(1)
        if time_match:
            time = time_match.group(1)

        meeting = {
            "type": "meeting",
            "date": date,
            "time": time
        }

        self.last_meeting = meeting
        self.workflow_state = "meeting_scheduled"
        self.ledger.append(meeting)

        return (
            f"Meeting scheduled on {date} at {time}.\n"
            "Follow-up will be prepared upon request."
        )

    # ------------------------------
    # Follow-Up Email
    # ------------------------------
    def send_follow_up(self) -> str:
        if self.workflow_state != "meeting_scheduled":
            return "No scheduled meeting found to follow up on."

        self.workflow_state = "follow_up_sent"

        self.ledger.append({
            "type": "follow_up_email",
            "status": "sent"
        })

        return (
            "Subject: Thank You for the Meeting\n\n"
            "Dear [Client Name],\n\n"
            "Thank you for your time today.\n"
            "Please let me know if you require any additional information.\n\n"
            "Best regards,\n"
            f"{self.name}"
        )

    # ------------------------------
    # Summarization
    # ------------------------------
    def summarize_text(self, text: str) -> str:
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return "\n".join(f"- {s}" for s in sentences if s)

    # ------------------------------
    # Administrative Report
    # ------------------------------
    def generate_report(self) -> str:
        report = [
            f"Administrative Report – {self.name}",
            "-" * 35,
            f"Current workflow state: {self.workflow_state}",
            "",
            "Completed actions:"
        ]

        if not self.ledger:
            report.append("- No administrative actions recorded.")
        else:
            for i, entry in enumerate(self.ledger, start=1):
                report.append(f"{i}. {entry}")

        report.append("")
        report.append("Pending next step:")

        if self.workflow_state == "intake_completed":
            report.append("- Schedule a meeting.")
        elif self.workflow_state == "meeting_scheduled":
            report.append("- Send follow-up email.")
        elif self.workflow_state == "follow_up_sent":
            report.append("- Await further instructions.")
        else:
            report.append("- Await administrative task.")

        return "\n".join(report)

    # ------------------------------
    # Main Response Handler
    # ------------------------------
    def respond(self, user_input: str) -> str:
        if not self.is_in_scope(user_input):
            response = (
                "I'm here strictly for administrative support. "
                "I cannot assist with that request."
            )

        elif "client intake" in user_input.lower():
            response = self.handle_client_intake()

        elif "schedule" in user_input.lower() or "meeting" in user_input.lower():
            response = self.schedule_meeting(user_input)

        elif "follow up" in user_input.lower():
            response = self.send_follow_up()

        elif "summarize" in user_input.lower():
            content = user_input.replace("summarize", "").strip()
            response = self.summarize_text(content)

        elif "report" in user_input.lower() or "status" in user_input.lower():
            response = self.generate_report()

        elif "email" in user_input.lower():
            response = self.send_follow_up()

        else:
            response = "Administrative request acknowledged."

        self.memory.append({
            "user": user_input,
            "sarah": response
        })

        return response

# ==============================
# End of Sarah Agent
# ==============================
