# day2_stress_test.py
# Day 2: Stress test for advanced multi-client operations
# Permanent storage path: /home/cloudstaff/cloudstaff-core/day2_stress_test.py

from day2_advanced_client import (
    onboard_client,
    schedule_meeting,
    send_followup,
    invoice_client,
    record_payment,
    client_report,
    overdue_clients,
)
import random

# --- Test clients ---
clients = ["Noah", "Olivia", "Ethan", "Sophia", "Liam"]

# --- Onboard clients ---
for client in clients:
    onboard_client(client)

# --- Schedule meetings & followups ---
for client in clients:
    schedule_meeting(client)
    send_followup(client)

# --- Invoice & payment scenarios ---
invoices = {
    "Noah": [100, 200, 150],
    "Olivia": [500, 300],
    "Ethan": [250, 250],
    "Sophia": [400, 100, 50],
    "Liam": [600]
}

payments = {
    "Noah": [100, 150, 200],
    "Olivia": [500, 300, 50],  # last payment should be rejected
    "Ethan": [250, 250],
    "Sophia": [500],
    "Liam": [600, 10]  # second payment should be rejected
}

# --- Insert invoices ---
for client, amounts in invoices.items():
    for amt in amounts:
        invoice_client(client, amt, description="Stress Test Invoice")

# --- Record payments ---
for client, amounts in payments.items():
    for amt in amounts:
        record_payment(client, amt)

# --- Generate client reports ---
for client in clients:
    print("-" * 50)
    client_report(client)

# --- Test overdue functionality ---
print("-" * 50)
overdue_clients(days=0)  # forcing all invoices to be overdue for test

# --- Random stress tests ---
print("-" * 50)
print("Random stress payments and invoices:")
for _ in range(20):
    client = random.choice(clients)
    action = random.choice(["invoice", "payment"])
    amount = random.randint(10, 500)
    if action == "invoice":
        invoice_client(client, amount, description="Random Invoice")
    else:
        record_payment(client, amount)

print("-" * 50)
print("Stress test complete.")
