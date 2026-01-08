from day3_advanced_client import get_all_clients, client_report, overdue_clients, high_value_clients, search_clients, notify_overdue

clients = get_all_clients()

print("\n--- DAY 3 STRESS TEST REPORT ---\n")

# 1. Reports
for client in clients:
    report = client_report(client)
    print(f"Client Report: {report['name']}")
    print(f"- Invoiced: {report['invoiced']}")
    print(f"- Paid: {report['paid']}")
    print(f"- Balance: {report['balance']}")
    print("-"*50)

# 2. Overdue notifications
print("\nOverdue clients (30+ days):")
notify_overdue()
print("-"*50)

# 3. High-value clients
print("\nHigh-value clients (>=1000 invoiced):")
for client in high_value_clients():
    print(f"- {client['client']}: {client['total_invoiced']}")
print("-"*50)

# 4. Semantic search tests
keywords = ["Noah", "Olivia", "Ethan", "Invoice"]
for kw in keywords:
    results = search_clients(kw)
    print(f"\nSearch results for '{kw}': {len(results)} entries")
    for r in results[:3]:  # only show top 3 for brevity
        print(r)
print("-"*50)

print("Day 3 stress test complete.")
