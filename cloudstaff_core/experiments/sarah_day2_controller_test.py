from cloudstaff_core.agents.controller import SarahController
from cloudstaff_core.agents.commands import Command


def divider(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def run():
    c = SarahController()

    divider("Illegal: Follow up from idle")
    print(c.execute(Command.SEND_FOLLOW_UP))

    divider("Client intake")
    print(c.execute(Command.CLIENT_INTAKE))

    divider("Illegal: Follow up before meeting")
    print(c.execute(Command.SEND_FOLLOW_UP))

    divider("Schedule meeting")
    print(c.execute(Command.SCHEDULE_MEETING, "on Friday at 10:00 AM"))

    divider("Send follow up")
    print(c.execute(Command.SEND_FOLLOW_UP))

    divider("Illegal: Schedule again")
    print(c.execute(Command.SCHEDULE_MEETING))


if __name__ == "__main__":
    run()

