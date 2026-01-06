# ==============================
# Upgraded Sarah Agent Definition
# ==============================

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
            "client intake responses"
        ]
        # Session memory for admin interactions
        self.memory: List[Dict[str, str]] = []

    # ------------------------------
    # System Prompt
    # ------------------------------
    def system_prompt(self) -> str:
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
        keywords = ["email", "calendar", "summarize", "client intake"]
        return any(word in user_input.lower() for word in keywords)

    # ------------------------------
    # Memory Recall
    # ------------------------------
    def recall_memory(self, n: int = 5) -> str:
        """Return the last n admin interactions."""
        if not self.memory:
            return "Memory is empty. No past admin interactions stored yet."
        response = f"Here are your last {min(n, len(self.memory))} admin interactions:\n"
        for i, entry in enumerate(self.memory[-n:], start=1):
            response += f"{i}. You: {entry['user']}\n   Sarah: {entry['sarah']}\n"
        return response

    # ------------------------------
    # Advanced Email Drafting
    # ------------------------------
    def draft_email(self, user_input: str) -> str:
        """Return a structured email template based on request."""
        subject = "[Your Subject Here]"
        body = (
            "Dear [Recipient],\n\n"
            "I hope this message finds you well.\n\n"
            "Best regards,\n"
            f"{self.name}\n[Your Job Title]\n[Your Company]\n[Your Contact Information]"
        )
        # Check for keywords to customize email type
        if "meeting" in user_input.lower():
            subject = "Meeting Confirmation"
            body = (
                "Dear [Client's Name],\n\n"
                "I am writing to confirm our upcoming meeting scheduled for [date] at [time].\n"
                "We will meet at [location/virtual platform link].\n\n"
                "Please let me know if there are any topics you'd like to discuss.\n\n"
                "Best regards,\n"
                f"{self.name}\n[Your Job Title]\n[Your Company]\n[Your Contact Information]"
            )
        elif "client intake" in user_input.lower():
            subject = "Welcome to [Your Company Name] - Client Intake Response"
            body = (
                "Dear [Client's Name],\n\n"
                "Thank you for reaching out to us at [Your Company Name].\n"
                "To better assist you, please provide the following information:\n"
                "1. Full Name\n"
                "2. Contact Information (phone and email)\n"
                "3. Brief description of your needs\n"
                "4. Preferred method of communication\n"
                "5. Any deadlines or timelines\n\n"
                "Once received, a team member will follow up promptly.\n\n"
                "Best regards,\n"
                f"{self.name}\n[Your Job Title]\n[Your Company Name]\n[Your Contact Information]\n[Your Company Website]"
            )
        return f"Subject: {subject}\n\n{body}"

    # ------------------------------
    # Summarization
    # ------------------------------
    def summarize_document(self, user_input: str) -> str:
        """Return a bullet-point summary placeholder for documents."""
        return "- Bullet point summary placeholder.\n- Highlight key points, dates, and tasks.\n- Ensure concise actionable items."

    # ------------------------------
    # Calendar Scheduling
    # ------------------------------
    def schedule_calendar(self, user_input: str) -> str:
        """Return a structured acknowledgment for calendar scheduling."""
        return "Calendar task acknowledged. Please provide participant details, time, and location if needed."

    # ------------------------------
    # Main Response Function
    # ------------------------------
    def respond(self, user_input: str) -> str:
        """
        Returns Sarah's response and stores it in session memory.
        Handles:
          - In-scope admin tasks
          - Memory recall
          - Strict refusal for out-of-scope tasks
        """
        in_scope = self.is_in_scope(user_input)

        # -------- Memory Recall Handling --------
        if "recall" in user_input.lower() or "memory" in user_input.lower():
            response = self.recall_memory(n=5)

        # -------- In-Scope Task Handling --------
        elif in_scope:
            if "email" in user_input.lower() or "meeting" in user_input.lower() or "client intake" in user_input.lower():
                response = self.draft_email(user_input)
            elif "summarize" in user_input.lower() or "report" in user_input.lower():
                response = self.summarize_document(user_input)
            elif "calendar" in user_input.lower() or "schedule" in user_input.lower():
                response = self.schedule_calendar(user_input)
            else:
                response = "Task recognized but not fully implemented yet."

        # -------- Out-of-Scope Refusal --------
        else:
            response = "I'm here strictly for administrative support. I cannot assist with that request."

        # -------- Store Interaction in Memory --------
        self.memory.append({"user": user_input, "sarah": response})
        return response

# ==============================
# End of Upgraded Sarah Agent
# ==============================
