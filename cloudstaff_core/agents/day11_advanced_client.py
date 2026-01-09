from cloudstaff_core.storage.event_store import log_event, load_events
from cloudstaff_core.storage.snapshot_engine import save_snapshot

clients = {}

def rebuild_state():
    events = load_events()
    for e in events:
        c = e["client"]
        clients.setdefault(c, {"invoiced": 0.0, "paid": 0.0})
        if e["action"] == "Invoice issued":
            clients[c]["invoiced"] += e["amount"]
        elif e["action"] == "Payment received":
            clients[c]["paid"] += e["amount"]

def invoice(client, amount):
    log_event(client, "Invoice issued", "Invoice", amount)

def payment(client, amount):
    log_event(client, "Payment received", "Invoice", amount)

def snapshot():
    save_snapshot(clients)
