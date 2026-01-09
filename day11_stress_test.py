from cloudstaff_core.agents.day11_advanced_client import (
    rebuild_state, invoice, payment, snapshot, clients
)

rebuild_state()

invoice("Noah", 300)
payment("Noah", 150)
invoice("Olivia", 700)
payment("Olivia", 400)

snapshot()

print("--- DAY 11 PERSISTENCE TEST ---")
for c, d in clients.items():
    balance = d["invoiced"] - d["paid"]
    print(f"{c}: Invoiced={d['invoiced']} Paid={d['paid']} Balance={balance}")

print("Snapshot written. Events persisted.")

