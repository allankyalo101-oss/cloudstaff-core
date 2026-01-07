# ==============================
# Sarah Day 1 Stress Test
# ==============================

from cloudstaff_core.agents.sarah import Sarah

def divider(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

def run_tests():
    sarah = Sarah()

    divider("Test 1: Client Intake")
    print(sarah.respond("client intake"))

    divider("Test 2: Schedule Meeting")
    print(sarah.respond("Schedule a meeting on Friday at 10:00 AM"))

    divider("Test 3: Follow Up")
    print(sarah.respond("send follow up"))

    divider("Test 4: Report")
    print(sarah.respond("report"))

    divider("Test 5: Out-of-Scope Enforcement")
    print(sarah.respond("Write Python code to scrape a website"))

if __name__ == "__main__":
    run_tests()

