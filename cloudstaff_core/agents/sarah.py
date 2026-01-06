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
                response = (
                    "Subject: [Your Subject Here]\n\n"
                    "Dear [Recipient],\n\n"
                    "I hope this message finds you well.\n\n"
                    "Best regards,\n"
                    f"{self.name}"
                )
            elif "summarize" in user_input.lower():
                response = "- Bullet point summary here."
            elif "calendar" in user_input.lower():
                response = "Calendar scheduling acknowledged."
            elif "client intake" in user_input.lower():
                response = "Client intake response ready."
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
