import re

class NaturalLanguageParser:
    """
    Converts simple natural language instructions into
    structured command strings for the CommandRouter.
    Enforces intent-safe parsing.
    """

    def parse(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""

        t = text.strip()
        tl = t.lower()

        name = self._extract_name(t)

        # Onboarding
        if re.search(r"\b(onboard|add|register)\b", tl):
            return f"onboard {name}"

        # Meeting
        if re.search(r"\b(schedule|set)\b.*\b(meeting|call)\b", tl):
            return f"meet {name}"

        # Follow-up
        if re.search(r"\b(follow up|follow-up|check in)\b", tl):
            return f"followup {name}"

        # Invoice (amount REQUIRED)
        if "invoice" in tl:
            amount = self._extract_amount(t)
            if amount is None:
                return "error missing_amount invoice"
            return f"invoice {name} {amount}"

        # Payment (amount REQUIRED)
        if "payment" in tl or "paid" in tl:
            amount = self._extract_amount(t)
            if amount is None:
                return "error missing_amount payment"
            return f"payment {name} {amount}"

        # Report
        if "report" in tl or "summary" in tl:
            return f"report {name}"

        return ""

    def _extract_name(self, text: str) -> str:
        words = text.split()
        for w in words:
            if w.istitle():
                return w
        return words[-1].capitalize()

    def _extract_amount(self, text: str):
        match = re.search(r"\b\d+(\.\d+)?\b", text)
        if not match:
            return None
        return float(match.group())
