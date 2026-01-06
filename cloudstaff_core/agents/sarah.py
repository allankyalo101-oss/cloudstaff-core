# ==============================
# Sarah Agent Core Definition
# ==============================

from typing import List
import re

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
        # Session memory for admin interactions
        self.memory = []
        self.sent_emails = []
        self.scheduled_meetings = []

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
        """Check if the task is within administrative scope."""
        keywords = ["email", "calendar", "summarize", "client intake", "meeting"]
        return any(word in user_input.lower() for word in keywords)

    # ------------------------------
    # Helper: Extract Client Info
    # ------------------------------
    def extract_client_info(self, user_input: str):
        """
        Try to extract client name, date, time, and topic from user input.
        Fallbacks used if missing.
        """
        client_name = "[Client Name]"
        date = "[Date]"
        time = "[Time]"
        topic = "[Topic]"

        match_client = re.search(r'client (\w+)', user_input, re.IGNORECASE)
        if match_client:
            client_name = match_client.group(1)

        match_date = re.search(r'on (\w+\s\d{1,2}(?:,\s\d{4})?)', user_input, re.IGNORECASE)
        if match_date:
            date = match_date.group(1)

        match_time = re.search(r'at (\d{1,2}:\d{2}\s?(?:AM|PM)?)', user_input, re.IGNORECASE)
        if match_time:
            time = match_time.group(1)

        match_topic = re.search(r'about ([\w\s]+)', user_input, re.IGNORECASE)
        if match_topic:
            topic = match_topic.group(1)

        return client_name, date, time, topic

    # ------------------------------
    # Helper: Format Email
    # ------------------------------
    def format_email(self, user_input: str, auto_subject: str = None) -> str:
        """Return a formatted email using dynamic placeholders extracted from input."""
        client_name, date, time, topic = self.extract_client_info(user_input)
        subject = auto_subject or (f"Regarding {topic}" if topic != "[Topic]" else "[Your Subject Here]")

        email = (
            f"Subject: {subject}\n\n"
            f"Dear {client_name},\n\n"
            f"I hope this message finds you well.\n"
            f"I am writing regarding {topic} scheduled for {date} at {time}.\n\n"
            "Please let me know if you require any additional information.\n\n"
            "Best regards,\n"
            f"{self.name}\n"
            "[Your Position]\n"
            "[Your Company]\n"
            "[Your Contact Information]"
        )
        self.sent_emails.append({
            "subject": subject,
            "recipient": client_name,
            "date": date,
            "time": time,
            "topic": topic
        })
        return email

    # ------------------------------
    # Helper: Schedule Meeting
    # ------------------------------
    def schedule_meeting(self, user_input: str = "") -> str:
        """
        Parse user input for participants, date, time, and platform.
        Schedule the meeting, store it in session memory,
        and auto-generate notification emails for participants.
        """
        participants = ["[Team Members]"]
        date = "[Date]"
        time = "[Time]"
        platform = "[Platform]"

        match_participants = re.search(r'with ([\w\s,]+)', user_input, re.IGNORECASE)
        if match_participants:
            participants = [p.strip() for p in match_participants.group(1).split(',')]

        match_date = re.search(r'on (\w+\s\d{1,2}(?:,\s\d{4})?)', user_input, re.IGNORECASE)
        if match_date:
            date = match_date.group(1)

        match_time = re.search(r'at (\d{1,2}:\d{2}\s?(?:AM|PM)?)', user_input, re.IGNORECASE)
        if match_time:
            time = match_time.group(1)

        match_platform = re.search(r'(on|via) (\w+)', user_input, re.IGNORECASE)
        if match_platform:
            platform = match_platform.group(2)

        meeting = {
            "participants": participants,
            "date": date,
            "time": time,
            "platform": platform
        }
        self.scheduled_meetings.append(meeting)

        # Auto-generate email notifications for participants
        email_responses = []
        for participant in participants:
            email_text = (
                f"Subject: Upcoming Meeting Notification\n\n"
                f"Dear {participant},\n\n"
                f"You are invited to a meeting on {date} at {time} via {platform}.\n"
                "Please confirm your attendance.\n\n"
                "Best regards,\n"
                f"{self.name}\n"
                "[Your Position]\n"
                "[Your Company]\n"
                "[Your Contact Information]"
            )
            self.sent_emails.append({
                "subject": "Upcoming Meeting Notification",
                "recipient": participant,
                "date": date,
                "time": time,
                "topic": "Meeting Invitation"
            })
            email_responses.append(email_text)

        participants_str = ", ".join(participants)
        response = (
            f"Meeting scheduled for {date} at {time} on {platform} with participants: {participants_str}.\n"
            "Notification emails have been generated for all participants.\n\n"
            "--- Email Previews ---\n"
            + "\n\n".join(email_responses)
        )

        return response

    # ------------------------------
    # Helper: Summarize Text
    # ------------------------------
    def summarize_text(self, text: str) -> str:
        sentences = re.split(r'(?<=[.!?]) +', text.strip())
        bullets = [f"- {s.strip()}" for s in sentences if s]
        return "\n".join(bullets) if bullets else "No content to summarize."

    # ------------------------------
    # Response Function
    # ------------------------------
    def respond(self, user_input: str) -> str:
        in_scope = self.is_in_scope(user_input)
        response = ""

        # -------- Memory Recall Handling --------
        if "recall" in user_input.lower() or "memory" in user_input.lower():
            if self.memory:
                response = "Here are your last admin interactions:\n"
                for i, entry in enumerate(self.memory[-5:], start=1):
                    response += f"{i}. You: {entry['user']}\n   Sarah: {entry['sarah']}\n"
            else:
                response = "Memory is empty. No past admin interactions stored yet."

        # -------- In-Scope Task Handling --------
        elif in_scope:
            if "email" in user_input.lower():
                response = self.format_email(user_input)

            elif "summarize" in user_input.lower():
                match = re.search(r'summarize (.+)', user_input, re.IGNORECASE)
                text_to_summarize = match.group(1) if match else "Provide text to summarize."
                response = self.summarize_text(text_to_summarize)

            elif "calendar" in user_input.lower() or "meeting" in user_input.lower():
                response = self.schedule_meeting(user_input)

            elif "client intake" in user_input.lower():
                response = (
                    "Subject: Welcome to [Your Company Name]! \n\n"
                    "Dear [Client Name],\n\n"
                    "Thank you for reaching out to us! Please provide:\n"
                    "1. Full Name\n2. Company Name (if applicable)\n3. Email\n4. Phone Number\n"
                    "5. Nature of Inquiry\n6. Preferred Method of Contact\n\n"
                    "Once we receive your information, we will get back promptly.\n\n"
                    "Best regards,\n"
                    f"{self.name}\n[Your Position]\n[Your Company]\n[Your Contact Information]"
                )

            else:
                response = "Task recognized but not fully implemented yet."

        # -------- Out-of-Scope Refusal --------
        else:
            response = "I'm here strictly for administrative support. I cannot assist with that request."

        # -------- Store Interaction in Memory --------
        self.memory.append({"user": user_input, "sarah": response})
        return response

# ==============================
# End of Sarah Agent Definition
# ==============================
