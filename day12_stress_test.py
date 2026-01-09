from cloudstaff_core.agents.day12_integrity_guard import integrity_check

print("\n--- DAY 12 INTEGRITY TEST ---")

try:
    integrity_check()
except RuntimeError as e:
    print("CRITICAL:", e)
else:
    print("System integrity confirmed.")

print("--- DAY 12 COMPLETE ---\n")

