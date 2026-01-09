from cloudstaff_core.agents.day10_advanced_client import (
    get_all_clients,
    client_report,
    search_clients,
    daily_notifications
)

import random

clients = get_all_clients()

# Stress-test: random invoices/payments
for client in clients:
    # Random invoices
    for _ in range(random.randint(1, 5)):
        amount = random.randint(50, 1000)
        print(f"Invoice of {amount} recorded for {client}.")
    # Random payments
    for _ in range(random.randint(1, 4)):
        amount = random.randint(50, 1000)
        print(f"Payment of {amount} received from {client}.")

# Generate client reports
print("--- DAY 10 STRESS TEST REPORT ---")
for client in clients:
    report = client_report(client)
    print(f"Client Report: {report['name']}")
    print(f"- Invoiced: {report['invoiced']}")
    print(f"- Paid: {report['paid']}")
    print(f"- Balance: {report['balance']}")
    print(f"- Avg Invoice: {report['avg_invoice']}")
    print(f"- Invoice Count: {report['invoice_count']}")
    print("--------------------------------------------------")

# Semantic search tests
keywords = ["Invoice", "Payment", "Noah", "Olivia"]
for kw in keywords:
    results = search_clients(kw)
    print(f"Search results for '{kw}': {len(results)} entries")
    for r in results[:3]:  # show first 3 only for brevity
        print(r)
    print("--------------------------------------------------")

# Automated notifications
print("Sending automated follow-ups and priority alerts:")
daily_notifications()
print("--------------------------------------------------")
print("Day 10 stress test complete.")

