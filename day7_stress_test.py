from cloudstaff_core.agents.day7_advanced_client import (
    get_all_clients, client_report, overdue_clients,
    high_value_clients, search_clients, send_followups_and_priority
)

clients_to_test = ["Alice", "Bob", "Charlie", "Noah", "Olivia", "Ethan", "Sophia", "Liam"]

# -----------------------
# Stress Test Execution
# -----------------------
print("--- DAY 7 STRESS TEST REPORT ---")

# Generate client reports
for client in clients_to_test:
    report = client_report(client)
    print(f"Client Report: {client}")
    print(f"- Invoiced: {report['invoiced']:.1f}")
    print(f"- Paid: {report['paid']:.1f}")
    print(f"- Balance: {report['balance']:.1f}")
    print(f"- Avg Invoice: {report['avg_invoice']:.2f}")
    print(f"- Invoice Count: {report['invoice_count']}")
    print("-" * 50)

# Show overdue clients
overdue = overdue_clients()
print("Overdue clients (30+ days):")
if overdue:
    for o in overdue:
        print(f"- {o['client']}: {o['amount']:.1f}")
else:
    print("None")
print("-" * 50)

# High-value clients
high_value = high_value_clients()
print("High-value clients (>=1000 invoiced):")
for c in high_value:
    print(f"- {c['client']}: {c['total_invoiced']:.1f}")
print("-" * 50)

# Semantic search examples
for keyword in ["Invoice", "Payment", "Noah", "Olivia"]:
    results = search_clients(keyword)
    print(f"Search results for '{keyword}': {len(results)} entries")
    for r in results[:3]:  # show top 3 for brevity
        print(r)
    print("-" * 50)

# Automated follow-ups and priority alerts
print("Sending automated follow-ups and priority alerts:")
send_followups_and_priority()
print("-" * 50)
print("Day 7 stress test complete.")

