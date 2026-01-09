from cloudstaff_core.agents.day4_advanced_client import (
    get_all_clients, client_report, overdue_clients,
    high_value_clients, search_clients, notify_overdue,
    record_invoice, record_payment, send_payment_reminders
)

# -----------------------
# Day 4 Stress Test
# -----------------------
clients = ["Noah", "Olivia", "Ethan", "Sophia", "Liam"]
invoice_amounts = [400, 1000, 500, 550, 600]
payment_amounts = [200, 1000, 500, 500, 600]

print("--- DAY 4 STRESS TEST REPORT ---\n")

# Step 1: Record invoices
for client, amount in zip(clients, invoice_amounts):
    record_invoice(client, amount, description="Day 4 Stress Invoice")

# Step 2: Record payments
for client, amount in zip(clients, payment_amounts):
    record_payment(client, amount)

# Step 3: Print client reports
for client in get_all_clients():
    report = client_report(client)
    print("Client Report:", report["name"])
    print(f"- Invoiced: {report['invoiced']}")
    print(f"- Paid: {report['paid']}")
    print(f"- Balance: {report['balance']}")
    print(f"- Avg Invoice: {report['avg_invoice']:.2f}")
    print(f"- Invoice Count: {report['invoice_count']}")
    print("--------------------------------------------------")

# Step 4: Overdue clients
overdue = overdue_clients()
print("Overdue clients (30+ days):")
if overdue:
    for entry in overdue:
        print(f"- {entry['client']}: {entry['amount']}")
else:
    print("None")
print("--------------------------------------------------")

# Step 5: High-value clients
high_value = high_value_clients()
print("High-value clients (>=1000 invoiced):")
for client in high_value:
    print(f"- {client['client']}: {client['total_invoiced']}")
print("--------------------------------------------------")

# Step 6: Semantic search demo
keywords = ["Noah", "Olivia", "Ethan", "Invoice"]
for keyword in keywords:
    results = search_clients(keyword)
    print(f"Search results for '{keyword}': {len(results)} entries")
    for r in results[:3]:  # show top 3 matches for brevity
        print(r)
    print("--------------------------------------------------")

# Step 7: Automated reminders
print("Sending automated payment reminders:")
send_payment_reminders()
print("--------------------------------------------------")

print("Day 4 stress test complete.")

