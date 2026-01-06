class Sarah:
    def __init__(self):
        self.name = "Sarah"
        self.role = "Administrative AI Assistant"
        self.scope = [
            "email drafting",
            "calendar scheduling",
            "basic document summarization",
            "client intake responses"
        ]
        # Persistent in-session memory
        self.memory = []

    def system_prompt(self):
        return (
            "You are Sarah, a professional administrative assistant AI. "
            "You communicate clearly, concisely, and politely. "
            "You do not perform tasks outside administrative support. "
            "Any request outside your scope must be refused with the exact message: "
            "'I'm here strictly for administrative support. I cannot assist with that request.'"
        )

    def is_in_scope(self, user_input: str) -> bool:
        user_input_lower = user_input.lower()
        for task in self.scope:
            if task in user_input_lower:
                return True
        return False

    def respond(self, user_input: str) -> str:
        """
        Returns Sarah's response and stores it in session memory.
        """
        if self.is_in_scope(user_input):
            # In-scope task handling
            if "email" in user_input.lower():
                response = (
                    "Subject: [Your Subject Here]\n\n"
                    "Dear [Recipient],\n\n"
                    "I hope this message finds you well.\n\n"
                    "Best regards,\n"
                    f"{self.name}"
                )
            elif "summarization" in user_input.lower():
                response = "- Bullet point summary here."
            elif "calendar" in user_input.lower():
                response = "Calendar scheduling acknowledged."
            elif "client intake" in user_input.lower():
                response = "Client intake response ready."
            else:
                response = "Task recognized but not fully implemented yet."
        else:
            # Out-of-scope task refusal
            response = "I'm here strictly for administrative support. I cannot assist with that request."

        # Store the interaction in memory
        self.memory.append({"user": user_input, "sarah": response})
        return response

    def recall_memory(self, n: int = 5):
        """
        Return the last n interactions from memory.
        """
        return self.memory[-n:]
