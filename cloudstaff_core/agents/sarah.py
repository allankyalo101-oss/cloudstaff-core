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
        # Session memory for admin interactions
        self.memory = []

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
    # Memory Recall
    # ------------------------------
    def recall_memory(self, last_n: int = 5) -> str:
        """Return last N admin interactions."""
        if not self.memory:
            return "Memory is empty. No past admin interactions stored yet."
        response = f"Last {min(last_n, len(self.memory))} admin interactions:\n"
        for i, entry in enumerate(self.memory[-last_n:], start=1):
            response += f"{i}. You: {entry['user']}\n   Sarah: {entry['sarah']}\n"
        return response

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
        user_lower = user_input.lower()
        in_scope = self.is_in_scope(user_input)

        # -------- Memory Recall Handling --------
        if "recall" in user_lower or "memory" in user_lower:
            response = self.recall_memory()

        # -------- In-Scope Task Handling --------
        elif in_scope:
            if "email" in user_lower:
                response = (
                    "Subject: [Your Subject Here]\n\n"
                    "Dear [Recipient],\n\n"
                    "I hope this message finds you well.\n\n"
                    "Best regards,\n"
                    f"{self.name}"
                )
            elif "summarize" in user_lower:
                response = "- Bullet point summary placeholder."
            elif "calendar" in user_lower:
                response = "Calendar scheduling acknowledged. Please provide details of date, time, and participants."
            elif "client intake" in user_lower:
                response = (
                    "Subject: Welcome to [Your Company Name] - Client Intake Response\n\n"
                    "Dear [Client's Name],\n\n"
                    "Thank you for reaching out to us. To assist you effectively, "
                    "please provide the following information:\n"
                    "1. Full Name\n"
                    "2. Contact Information (email and phone)\n"
                    "3. Brief description of your inquiry\n"
                    "4. Preferred method of contact (email, phone, etc.)\n"
                    "5. Any deadlines or timelines\n\n"
                    "Once we receive your response, a member of our team will follow up promptly.\n\n"
                    "Best regards,\n"
                    f"{self.name}\n"
                    "[Your Job Title]\n"
                    "[Your Company Name]\n"
                    "[Your Contact Information]\n"
                    "[Your Company Website]"
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
