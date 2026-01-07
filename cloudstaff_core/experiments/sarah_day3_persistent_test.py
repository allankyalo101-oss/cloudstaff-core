# ==============================
# Sarah Day 3 Persistent Stress Test
# ==============================

from cloudstaff_core.agents.sarah import Sarah

def divider(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

def run_tests():
    sarah = Sarah()

    divider("Initial State / Resume")
    print(f"Current workflow state: {sarah.workflow_state}")
    print(f"Logged actions: {len(sarah.ledger)}")

    divider("Attempt Illegal Action")
    print(sarah.respond("send follow up"))  # Should be blocked if no meeting

    divider("Perform Client Intake")
    print(sarah.respond("client intake"))

    divider("Schedule Meeting")
    print(sarah.respond("schedule meeting on Friday at 10:00 AM"))

    divider("Send Follow-Up")
    print(sarah.respond("send follow up"))

    divider("Generate Report")
    print(sarah.respond("report"))

    divider("Reset System")
    print(sarah.respond("reset"))

    divider("Post-Reset Check")
    print(f"Current workflow state: {sarah.workflow_state}")
    print(f"Logged actions: {len(sarah.ledger)}")

if __name__ == "__main__":
    run_tests()
