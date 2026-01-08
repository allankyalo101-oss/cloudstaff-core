from cloudstaff_core.commands.command_router import CommandRouter
from cloudstaff_core.commands.nl_parser import NaturalLanguageParser

def run():
    router = CommandRouter()
    parser = NaturalLanguageParser()

    inputs = [
        # Noah begins
        "Please onboard client Noah",

        # Olivia begins before Noah finishes
        "Please onboard client Olivia",

        # Interleaved progression
        "Schedule a meeting with Noah",
        "Schedule a meeting with Olivia",

        "Send a follow up to Noah",
        "Send a follow up to Olivia",

        # Diverging economics
        "Invoice Noah 400",
        "Invoice Olivia 1000",

        "Noah paid 200",
        "Olivia paid 1000",

        # Reports must be isolated and correct
        "Give me a report for Noah",
        "Give me a report for Olivia",
    ]

    for text in inputs:
        command = parser.parse(text)
        print(f"> {text}")
        print(f"→ {command}")
        print(router.execute(command))
        print("-" * 50)

if __name__ == "__main__":
    run()
