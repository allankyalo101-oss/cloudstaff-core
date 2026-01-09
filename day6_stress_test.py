# File: cloudstaff-core/day6_stress_test.py

from cloudstaff_core.agents.day6_advanced_client import (
    get_all_clients,
    client_report,
    overdue_clients,
    high_value_clients,
    search_clients,
    automated_followups,
    notify_overdue
)


# -----------------------
# Day 6 Stress Test
# -----------------------
if __name__ == "__main__":
    print("--- DAY 6 STRESS TEST REPORT ---")

    clients = get_all_clients()

    # 1. Generate full client reports
    for client in clients:
        report = client_report(client)
        print(f"Client Report: {report['name']}")
        print(f"- Invoiced: {report['invoiced']:.2f}")
        print(f"- Paid: {report['paid']:.2f}")
        print(f"- Balance: {report['balance']:.2f}")
        print(f"- Avg Invoice: {report['avg_invoice']:.2f}")
        print(f"- Invoice Count: {report['invoice_count']}")
        print(f"- Payment Completion: {report['payment_pct']:.1f}%")
        print("--------------------------------------------------")

    # 2. Overdue clients
    overdue = overdue_clients()
    print("Overdue clients (30+ days):")
    if overdue:
        for entry in overdue:
            print(f"- {entry['client']}: {entry['amount']:.2f}")
    else:
        print("None")
    print("--------------------------------------------------")

    # 3. High-value clients
    high_value = high_value_clients()
    print("High-value clients (>=1000 invoiced):")
    if high_value:
        for entry in high_value:
            print(f"- {entry['client']}: {entry['total_invoiced']:.2f}")
    else:
        print("None")
    print("--------------------------------------------------")

    # 4. Semantic searches
    keywords = ["Invoice", "Payment", "Noah", "Olivia", "Ethan"]
    for kw in keywords:
        results = search_clients(kw)
        print(f"Search results for '{kw}': {len(results)} entries")
        for r in results[:3]:  # Show top 3 for brevity
            print(r)
        print("--------------------------------------------------")

    # 5. Automated follow-ups
    print("Sending automated follow-ups and priority alerts:")
    automated_followups()
    notify_overdue()
    print("--------------------------------------------------")
    print("Day 6 stress test complete.")

