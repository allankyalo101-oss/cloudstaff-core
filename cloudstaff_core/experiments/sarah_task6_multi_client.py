# cloudstaff_core/experiments/sarah_task6_multi_client.py

from cloudstaff_core.commands.command_router import CommandRouter
from cloudstaff_core.commands.nl_parser import NaturalLanguageParser

def run_task6():
    router = CommandRouter()
    parser = NaturalLanguageParser()

    # Multi-client simulation inputs
    inputs = [
        # Client Noah
        "Please onboard client Noah",
        "Schedule a meeting with Noah",
        "Send a follow up to Noah",
        "Invoice Noah 400",
        "Noah paid 200",
        "Noah paid 200",
        "Noah paid 1",  # should fail: already settled
        "Give me a report for Noah",

        # Client Olivia
        "Please onboard client Olivia",
        "Schedule a meeting with Olivia",
        "Send a follow up to Olivia",
        "Invoice Olivia 1000",
        "Olivia paid 1000",
        "Olivia paid 50",  # should fail: already settled
        "Give me a report for Olivia",

        # Client Ethan
        "Please onboard client Ethan",
        "Invoice Ethan 500",  # should fail: skipped steps
        "Schedule a meeting with Ethan",
        "Send a follow up to Ethan",
        "Invoice Ethan 500",
        "Ethan paid 500",
        "Give me a report for Ethan",
    ]

    for text in inputs:
        command = parser.parse(text)
        print(f"> {text}")
        print(f"→ {command}")
        print(router.execute(command))
        print("-" * 50)

if __name__ == "__main__":
    run_task6()
