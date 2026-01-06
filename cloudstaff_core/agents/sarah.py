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

        # Allowed scope
        self.scope = [
            "email drafting",
            "calendar scheduling",
            "document summarization",
            "client intake",
            "administrative follow-up"
        ]

        # Core memory
        self.memory: List[Dict] = []

        # Administrative ledger (business artifacts)
        self.ledger: List[Dict] = []

        # Context anchors
        self.last_client = None
        self.last_meeting = None

        # Workflow state
        self.workflow_state = "idle"

    # ------------------------------
    # System Prompt
    # ------------------------------
    def system_prompt(self):
        return (
            "You are Sarah, a professional administrative assistant AI. "
            "You operate strictly within administrative support. "
            "You track tasks, meetings, and follow-ups accurately."
        )

    # ------------------------------
    # Scope Checker
    # ------------------------------
    def is_in_scope(self, user_input: str) -> bool:
        keywords = [
            "email", "meeting", "schedule",
            "summarize", "client intake",
            "follow up"
        ]
        return any(k in user_input.lower() for k in keywords)

    # ------------------------------
    # Client Intake
    # ------------------------------
    def handle_client_intake(self) -> str:
        self.workflow_state = "intake_completed"

        intake = {
            "type": "client_intake",
            "status": "completed"
        }
        self.ledger.append(intake)

        return (
            "Thank you for your inquiry.\n\n"
            "To proceed, please share:\n"
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
        platform = "[Platform]"

        date_match = re.search(r'on ([\w\s\d]+)', user_input, re.IGNORECASE)
        time_match = re.search(r'at (\d{1,2}:\d{2}\s?(AM|PM)?)', user_input, re.IGNORECASE)

        if date_match:
            date = date_match.group(1)
        if time_match:
            time = time_match.group(1)

        meeting = {
            "type": "meeting",
            "date": date,
            "time": time,
            "platform": platform
        }

        self.last_meeting = meeting
        self.workflow_state = "meeting_scheduled"
        self.ledger.append(meeting)

        return (
            f"Meeting scheduled on {date} at {time}.\n"
            "I will prepare a follow-up email after the meeting."
        )

    # ------------------------------
    # Follow-Up Email
    # ------------------------------
    def send_follow_up(self) -> str:
        if self.workflow_state != "meeting_scheduled":
            return "No meeting on record to follow up on."

        self.workflow_state = "follow_up_sent"

        follow_up = {
            "type": "follow_up_email",
            "status": "sent"
        }
        self.ledger.append(follow_up)

        return (
            "Subject: Thank You for the Meeting\n\n"
            "Dear [Client Name],\n\n"
            "Thank you for taking the time to meet with us.\n"
            "Please let me know if you need any additional information.\n\n"
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
