from cloudstaff_core.agents.day3_advanced_client import (
    get_all_clients,
    client_report,
    overdue_clients,
    high_value_clients,
    search_clients,
    notify_overdue,
)

print("\n--- DAY 3 STRESS TEST REPORT ---\n")

# -----------------------
# Client reports
# -----------------------
for client in get_all_clients():
    report = client_report(client)
    print(f"Client Report: {report['name']}")
    print(f"- Invoiced: {report['invoiced']}")
    print(f"- Paid: {report['paid']}")
    print(f"- Balance: {report['balance']}")
    print("-" * 50)

# -----------------------
# Overdue clients
# -----------------------
print("\nOverdue clients (30+ days):")
overdue = overdue_clients()
if overdue:
    for entry in overdue:
        print(f"- {entry['client']}: {entry['amount']}")
else:
    print("None")
print("-" * 50)

# -----------------------
# High value clients
# -----------------------
print("\nHigh-value clients (>=1000 invoiced):")
high_value = high_value_clients()
for client in high_value:
    print(f"- {client['client']}: {client['total_invoiced']}")
print("-" * 50)

# -----------------------
# Semantic search tests
# -----------------------
for term in ["Noah", "Olivia", "Ethan", "Invoice"]:
    results = search_clients(term)
    print(f"\nSearch results for '{term}': {len(results)} entries")
    for r in results[:3]:
        print(r)

print("-" * 50)

# -----------------------
# Notifications
# -----------------------
notify_overdue()

print("\nDay 3 stress test complete.")
