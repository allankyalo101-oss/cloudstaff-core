from cloudstaff_core.agents.day9_advanced_client import (
    get_all_clients,
    client_report,
    overdue_clients,
    high_value_clients,
    search_clients,
    notify_overdue,
    notify_priority
)

clients_to_test = ["Alice", "Bob", "Charlie", "Noah", "Olivia", "Ethan", "Sophia", "Liam"]

print("--- DAY 9 STRESS TEST REPORT ---\n")

# Generate reports
for client in clients_to_test:
    report = client_report(client)
    print(f"Client Report: {report['name']}")
    print(f"- Invoiced: {report['invoiced']}")
    print(f"- Paid: {report['paid']}")
    print(f"- Balance: {report['balance']}")
    print(f"- Avg Invoice: {report['avg_invoice']}")
    print(f"- Invoice Count: {report['invoice_count']}")
    print("--------------------------------------------------")

# Overdue clients
overdue = overdue_clients()
print("Overdue clients (30+ days):")
if overdue:
    for entry in overdue:
        print(f"- {entry['client']}: {entry['amount']}")
else:
    print("None")
print("--------------------------------------------------")

# High-value clients
high_value = high_value_clients()
print("High-value clients (>=1000 invoiced):")
for entry in high_value:
    print(f"- {entry['client']}: {entry['total_invoiced']}")
print("--------------------------------------------------")

# Search tests
search_terms = ["Invoice", "Payment", "Noah", "Olivia", "Ethan"]
for term in search_terms:
    results = search_clients(term)
    print(f"Search results for '{term}': {len(results)} entries")
    for r in results[:3]:  # show only first 3 for brevity
        print(r)
    print("--------------------------------------------------")

# Automated notifications
print("Sending automated follow-ups and priority alerts:")
notify_overdue()
notify_priority()
print("--------------------------------------------------")
print("Day 9 stress test complete.")

