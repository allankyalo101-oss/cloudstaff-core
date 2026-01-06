# ==============================
# Sarah Agent Core Definition
# ==============================

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
        # Session memory for admin interactions and sent emails
        self.memory = []
        self.sent_emails = []

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
        keywords = ["email", "calendar", "summarize", "client intake"]
        return any(word in user_input.lower() for word in keywords)

    # ------------------------------
    # Helper: Format Email
    # ------------------------------
    def format_email(self, subject: str, recipient: str = "[Client Name]", date: str = "[Date]",
                     time: str = "[Time]", topic: str = "[Topic]") -> str:
        """Return a formatted email template with dynamic placeholders."""
        email = (
            f"Subject: {subject}\n\n"
            f"Dear {recipient},\n\n"
            f"I hope this message finds you well.\n"
            f"I am writing regarding {topic} scheduled for {date} at {time}.\n\n"
            "Please let me know if you require any additional information.\n\n"
            "Best regards,\n"
            f"{self.name}\n"
            "[Your Position]\n"
            "[Your Company]\n"
            "[Your Contact Information]"
        )
        # Track sent email in memory
        self.sent_emails.append({"subject": subject, "recipient": recipient, "date": date, "time": time, "topic": topic})
        return email

    # ------------------------------
    # Response Function
    # ------------------------------
    def respond(self, user_input: str) -> str:
        """
        Returns Sarah's response and stores it in session memory.
        Handles:
          - In-scope admin tasks
          - Memory recall for admin interactions
          - Strict refusal for out-of-scope tasks
        """
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
                # Provide dynamic placeholders for user to fill
                response = self.format_email(subject="[Your Subject Here]")

            elif "summarize" in user_input.lower():
                response = "- Bullet point summary here."

            elif "calendar" in user_input.lower():
                response = "Calendar scheduling acknowledged."

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
