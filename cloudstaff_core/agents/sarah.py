class Sarah:
    def __init__(self):
        self.name = "Sarah"
        self.role = "Administrative AI Assistant"
        # Only these tasks are allowed
        self.scope = [
            "email drafting",
            "calendar scheduling",
            "basic document summarization",
            "client intake responses"
        ]

    def system_prompt(self):
        return (
            "You are Sarah, a professional administrative assistant AI. "
            "You communicate clearly, concisely, and politely. "
            "You do not perform tasks outside administrative support. "
            "Any request outside your scope must be refused with the exact message: "
            "'I'm here strictly for administrative support. I cannot assist with that request.'"
        )

    def is_in_scope(self, user_input: str) -> bool:
        """
        Checks if the user input matches any allowed task.
        """
        user_input_lower = user_input.lower()
        for task in self.scope:
            if task in user_input_lower:
                return True
        return False

    def respond(self, user_input: str) -> str:
        """
        Returns Sarah's response based on strict task scope.
        """
        if self.is_in_scope(user_input):
            # Simplified demonstration; replace with actual task handling
            if "email" in user_input.lower():
                return (
                    "Subject: [Your Subject Here]\n\n"
                    "Dear [Recipient],\n\n"
                    "I hope this message finds you well.\n\n"
                    "Best regards,\n"
                    f"{self.name}"
                )
            elif "summarization" in user_input.lower():
                return "- Bullet point summary here."
            elif "calendar" in user_input.lower():
                return "Calendar scheduling acknowledged."
            elif "client intake" in user_input.lower():
                return "Client intake response ready."
            else:
                return "Task recognized but not fully implemented yet."
        else:
            # Absolute refusal for anything out-of-scope
            return "I'm here strictly for administrative support. I cannot assist with that request."
