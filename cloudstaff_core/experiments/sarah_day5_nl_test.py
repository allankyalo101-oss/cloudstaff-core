from cloudstaff_core.commands.command_router import CommandRouter
from cloudstaff_core.commands.nl_parser import NaturalLanguageParser

def run():
    router = CommandRouter()
    parser = NaturalLanguageParser()

    inputs = [
        "Please onboard client Ethan",
        "Schedule a meeting with Ethan",
        "Send a follow up to Ethan",
        "Invoice Ethan 400",
        "Ethan paid 200",
        "Give me a report for Ethan"
    ]

    for text in inputs:
        command = parser.parse(text)
        print(f"> {text}")
        print(f"→ {command}")
        print(router.execute(command))
        print("-" * 40)

if __name__ == "__main__":
    run()
