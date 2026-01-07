import re

class NaturalLanguageParser:
    """
    Converts simple natural language instructions into
    structured command strings for the CommandRouter.
    """

    def parse(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""

        t = text.lower().strip()

        # Onboarding
        if re.search(r"(onboard|add|register).*(client|customer)?", t):
            return f"onboard {self._extract_name(t)}"

        # Meeting
        if re.search(r"(schedule|set).*(meeting|call)", t):
            return f"meet {self._extract_name(t)}"

        # Follow-up
        if re.search(r"(follow up|follow-up|check in)", t):
            return f"followup {self._extract_name(t)}"

        # Invoice
        if "invoice" in t:
            amount = self._extract_amount(t)
            return f"invoice {self._extract_name(t)} {amount}"

        # Payment
        if "payment" in t or "paid" in t:
            amount = self._extract_amount(t)
            return f"payment {self._extract_name(t)} {amount}"

        # Report
        if "report" in t or "summary" in t:
            return f"report {self._extract_name(t)}"

        return ""

    def _extract_name(self, text: str) -> str:
        words = text.split()
        for w in words:
            if w.istitle():
                return w
        return words[-1].capitalize()

    def _extract_amount(self, text: str) -> float:
        matches = re.findall(r"\d+(\.\d+)?", text)
        return float(matches[0]) if matches else 0.0
