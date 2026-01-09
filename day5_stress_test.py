from cloudstaff_core.agents.day5_advanced_client import (
    get_all_clients, client_report, overdue_clients,
    high_value_clients, search_clients, notify_overdue,
    bulk_invoice, bulk_payment
)
from datetime import datetime, timedelta
import random

print("--- DAY 5 STRESS TEST REPORT ---")

# -----------------------
# Step 1: Define clients and random invoices/payments
# -----------------------
clients = get_all_clients()
random_invoices = [random.randint(100, 1000) for _ in clients]
random_payments = [random.randint(50, amt) for amt in random_invoices]

# -----------------------
# Step 2: Apply bulk invoices
# -----------------------
bulk_invoice(clients, random_invoices)
for c, amt in zip(clients, random_invoices):
    print(f"Invoice of {amt} recorded for {c}.")

# -----------------------
# Step 3: Apply bulk payments
# -----------------------
bulk_payment(clients, random_payments)
for c, amt in zip(clients, random_payments):
    print(f"Payment of {amt} received from {c}.")

# -----------------------
# Step 4: Generate client reports
# -----------------------
for client in clients:
    report = client_report(client)
    print(f"Client Report: {report['name']}")
    print(f"- Invoiced: {report['invoiced']}")
    print(f"- Paid: {report['paid']}")
    print(f"- Balance: {report['balance']}")
    print(f"- Avg Invoice: {report['avg_invoice']:.2f}")
    print(f"- Invoice Count: {report['invoice_count']}")
    print("-" * 50)

# -----------------------
# Step 5: Overdue clients
# -----------------------
overdue = overdue_clients(days=15)  # shorter window for stress
if overdue:
    print("Overdue clients (15+ days):")
    for entry in overdue:
        print(f"- {entry['client']}: {entry['amount']}")
else:
    print("Overdue clients (15+ days): None")
print("-" * 50)

# -----------------------
# Step 6: High-value clients
# -----------------------
high_value = high_value_clients(threshold=1500)
if high_value:
    print("High-value clients (>=1500 invoiced):")
    for entry in high_value:
        print(f"- {entry['client']}: {entry['total_invoiced']}")
else:
    print("High-value clients (>=1500 invoiced): None")
print("-" * 50)

# -----------------------
# Step 7: Semantic search test
# -----------------------
keywords = ['Invoice', 'Payment', 'Noah', 'Olivia']
for kw in keywords:
    results = search_clients(kw)
    print(f"Search results for '{kw}': {len(results)} entries")
    for r in results[:3]:  # show top 3 matches
        print(r)
    print("-" * 50)

# -----------------------
# Step 8: Overdue notifications
# -----------------------
print("Sending automated payment reminders:")
notify_overdue()
print("-" * 50)

print("Day 5 stress test complete.")

