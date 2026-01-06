# ==============================
# Sarah Agent Core Definition
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
            "basic document summarization",
            "client intake responses"
        ]

        # Core administrative memory
        self.memory: List[Dict] = []

        # Structured admin intelligence
        self.sent_emails: List[Dict] = []
        self.scheduled_meetings: List[Dict] = []

        # Context anchors
        self.last_client = None
        self.last_meeting = None
        self.last_participants = []

    # ------------------------------
    # System Prompt
    # ------------------------------
    def system_prompt(self):
        return (
            "You are Sarah, a professional administrative assistant AI. "
            "You communicate clearly, concisely, and politely. "
            "You do not perform tasks outside administrative support."
        )

    # ------------------------------
    # Scope Checker
    # ------------------------------
    def is_in_scope(self, user_input: str) -> bool:
        keywords = [
            "email", "calendar", "meeting",
            "summarize", "client intake",
            "follow up", "schedule"
        ]
        return any(k in user_input.lower() for k in keywords)

    # ------------------------------
    # Context Resolution
    # ------------------------------
    def resolve_context(self):
        return {
            "client": self.last_client or "[Client Name]",
            "meeting": self.last_meeting or {
                "date": "[Date]",
                "time": "[Time]",
                "platform": "[Platform]"
            },
            "participants": self.last_participants or ["[Participant]"]
        }

    # ------------------------------
    # Email Composer
    # ------------------------------
    def compose_email(self, user_input: str) -> str:
        context = self.resolve_context()

        subject = "Follow-Up"
        if "meeting" in user_input.lower():
            subject = "Meeting Follow-Up"

        email = (
            f"Subject: {subject}\n\n"
            f"Dear {context['client']},\n\n"
            "I hope this message finds you well.\n"
            "I am following up regarding our recent discussion.\n\n"
            "Please let me know if you require any additional information.\n\n"
            "Best regards,\n"
            f"{self.name}\n"
            "[Your Position]\n"
            "[Your Company]\n"
            "[Your Contact Information]"
        )

        self.sent_emails.append({
            "recipient": context["client"],
            "subject": subject
        })

        self.last_client = context["client"]
        return email

    # ------------------------------
    # Meeting Scheduler
    # ------------------------------
    def schedule_meeting(self, user_input: str) -> str:
        context = self.resolve_context()

        date = context["meeting"]["date"]
        time = context["meeting"]["time"]
        platform = context["meeting"]["platform"]
        participants = context["participants"]

        date_match = re.search(r'on (\w+\s\d{1,2})', user_input, re.IGNORECASE)
        time_match = re.search(r'at (\d{1,2}:\d{2}\s?(?:AM|PM)?)', user_input, re.IGNORECASE)
        platform_match = re.search(r'(via|on) (\w+)', user_input, re.IGNORECASE)

        if date_match:
            date = date_match.group(1)
        if time_match:
            time = time_match.group(1)
        if platform_match:
            platform = platform_match.group(2)

        meeting = {
            "date": date,
            "time": time,
            "platform": platform,
            "participants": participants
        }

        self.scheduled_meetings.append(meeting)
        self.last_meeting = meeting
        self.last_participants = participants

        return (
            f"Meeting scheduled on {date} at {time} via {platform}.\n"
            f"Participants: {', '.join(participants)}.\n"
            "I will prepare follow-up communication as needed."
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
        response = ""

        if not self.is_in_scope(user_input):
            response = (
                "I'm here strictly for administrative support. "
                "I cannot assist with that request."
            )

        elif "email" in user_input.lower() or "follow up" in user_input.lower():
            response = self.compose_email(user_input)

        elif "meeting" in user_input.lower() or "schedule" in user_input.lower():
            response = self.schedule_meeting(user_input)

        elif "summarize" in user_input.lower():
            content = user_input.replace("summarize", "").strip()
            response = self.summarize_text(content)

        elif "client intake" in user_input.lower():
            response = (
                "Subject: Welcome to [Your Company Name]\n\n"
                "Dear [Client Name],\n\n"
                "Thank you for reaching out. Please provide:\n"
                "1. Full Name\n2. Company Name\n3. Email\n4. Phone Number\n"
                "5. Nature of Inquiry\n\n"
                "We will respond promptly.\n\n"
                "Best regards,\n"
                f"{self.name}"
            )

        self.memory.append({
            "user": user_input,
            "sarah": response
        })

        return response

# ==============================
# End of Sarah Agent Definition
# ==============================
