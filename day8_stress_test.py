from cloudstaff_core.agents.day8_advanced_client import (
    get_all_clients,
    client_report,
    overdue_clients,
    high_value_clients,
    search_clients,
    notify_overdue,
    notify_high_value
)

import random

# -----------------------
# Stress test for Day 8
# -----------------------
clients = get_all_clients()
invoice_options = [100, 200, 250, 400, 500, 600]

print("--- DAY 8 STRESS TEST REPORT ---")

# Generate random invoices and payments
for client in clients:
    for _ in range(random.randint(1, 5)):
        invoice_amount = random.choice(invoice_options)
        # Record invoice (simulate)
        print(f"Invoice of {invoice_amount} recorded for {client}.")
    for _ in range(random.randint(1, 5)):
        payment_amount = random.choice(invoice_options)
        # Record payment (simulate)
        print(f"Payment of {payment_amount} received from {client}.")

# Generate client reports
for client in clients:
    report = client_report(client)
    print(f"Client Report: {report['name']}")
    print(f"- Invoiced: {report['invoiced']:.2f}")
    print(f"- Paid: {report['paid']:.2f}")
    print(f"- Balance: {report['balance']:.2f}")
    print(f"- Avg Invoice: {report['avg_invoice']:.2f}")
    print(f"- Invoice Count: {report['invoice_count']}")
    print("--------------------------------------------------")

# Overdue and high-value alerts
if overdue_clients():
    print("Overdue clients (30+ days):")
    notify_overdue()
else:
    print("Overdue clients (30+ days): None")
print("--------------------------------------------------")

print("High-value clients (>=1000 invoiced):")
notify_high_value()
print("--------------------------------------------------")

# Semantic searches
keywords = ["Invoice", "Payment", "Noah", "Olivia", "Ethan"]
for kw in keywords:
    results = search_clients(kw)
    print(f"Search results for '{kw}': {len(results)} entries")
    for r in results[:3]:
        print(r)
    print("--------------------------------------------------")

print("Sending automated follow-ups and priority alerts:")
notify_overdue()
notify_high_value()
print("--------------------------------------------------")
print("Day 8 stress test complete.")

