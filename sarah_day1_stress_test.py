# ==============================
# Sarah Day 1 Stress Test with Verification
# ==============================
import sys
import os
sys.path.insert(0, os.path.abspath("./cloudstaff_core"))

from agents.sarah import Sarah
from cloudstaff_core.agents.sarah import Sarah

# Initialize Sarah
sarah = Sarah()

# ------------------------------
# Helper function to print header
# ------------------------------
def print_header(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50 + "\n")

# ------------------------------
# Helper function for verification
# ------------------------------
def verify_step(description, expected_state=None, expected_ledger_inc=1):
    actual_state = sarah.workflow_state
    ledger_count = len(sarah.ledger)
    memory_count = len(sarah.memory)
    print(f"[VERIFY] {description}")
    if expected_state:
        assert actual_state == expected_state, f"Expected state '{expected_state}', got '{actual_state}'"
    assert ledger_count >= expected_ledger_inc, f"Expected at least {expected_ledger_inc} ledger entries, got {ledger_count}"
    print(f"State: {actual_state}, Ledger entries: {ledger_count}, Memory entries: {memory_count}\n")

# ------------------------------
# 1. Test Client Intake
# ------------------------------
print_header("Test 1: Client Intake")
response = sarah.respond("client intake")
print(f"Sarah: {response}")
verify_step("Client intake completed", expected_state="intake_completed")

# ------------------------------
# 2. Test Meeting Scheduling
# ------------------------------
print_header("Test 2: Schedule Meeting")
response = sarah.respond("Schedule a meeting on Friday at 10:00 AM")
print(f"Sarah: {response}")
verify_step("Meeting scheduled", expected_state="meeting_scheduled")

# ------------------------------
# 3. Test Follow-Up Email
# ------------------------------
print_header("Test 3: Send Follow-Up")
response = sarah.respond("send follow up")
print(f"Sarah: {response}")
verify_step("Follow-up sent", expected_state="follow_up_sent")

# ------------------------------
# 4. Test Summarization
# ------------------------------
print_header("Test 4: Summarize Text")
text_to_summarize = "Sarah scheduled a meeting. A follow-up was sent. The client responded positively."
response = sarah.respond(f"summarize {text_to_summarize}")
print(f"Sarah: {response}")
verify_step("Text summarized")  # no workflow change expected

# ------------------------------
# 5. Test Report Generation
# ------------------------------
print_header("Test 5: Generate Report")
response = sarah.respond("report")
print(f"Sarah: {response}")
verify_step("Report generated")  # no workflow change expected

# ------------------------------
# 6. Test Status Command
# ------------------------------
print_header("Test 6: Status Command")
response = sarah.respond("status")
print(f"Sarah: {response}")
verify_step("Status requested")  # no workflow change expected

# ------------------------------
# 7. Test Reset Command
# ------------------------------
print_header("Test 7: Reset System")
response = sarah.respond("reset")
print(f"Sarah: {response}")
verify_step("System reset", expected_state="idle", expected_ledger_inc=0)

# ------------------------------
# 8. Test Out-of-Scope Request
# ------------------------------
print_header("Test 8: Out-of-Scope Input")
response = sarah.respond("Write Python code to scrape a website")
print(f"Sarah: {response}")
verify_step("Out-of-scope request handled", expected_state="idle")  # state should not change

# ------------------------------
# 9. Test Follow-Up Before Meeting (Edge Case)
# ------------------------------
print_header("Test 9: Follow-Up Before Meeting (Edge Case)")
sarah.workflow_state = "idle"  # ensure no meeting scheduled
response = sarah.respond("send follow up")
print(f"Sarah: {response}")
verify_step("Follow-up without meeting handled", expected_state="idle")  # state should remain idle

# ------------------------------
# 10. Test Multiple Client Intakes
# ------------------------------
print_header("Test 10: Multiple Client Intakes")
for i in range(1, 4):
    response = sarah.respond("client intake")
    print(f"Sarah: {response}")
verify_step("Multiple client intakes", expected_state="intake_completed")

# ------------------------------
# Stress Test Summary
# ------------------------------
print_header("Stress Test Completed")
print("Final Workflow State:", sarah.workflow_state)
print("Total Memory Entries:", len(sarah.memory))
print("Total Ledger Entries:", len(sarah.ledger))

