from cloudstaff_core.commands.command_router import CommandRouter
from cloudstaff_core.commands.nl_parser import NaturalLanguageParser

def run():
    router = CommandRouter()
    parser = NaturalLanguageParser()

    inputs = [
        "Please onboard client Noah",
        "Schedule a meeting with Noah",
        "Send a follow up to Noah",
        "Invoice Noah 400",
        "Noah paid 200",
        "Give me a report for Noah"
    ]

    for text in inputs:
        command = parser.parse(text)
        print(f"> {text}")
        print(f"→ {command}")
        print(router.execute(command))
        print("-" * 40)

if __name__ == "__main__":
    run()
