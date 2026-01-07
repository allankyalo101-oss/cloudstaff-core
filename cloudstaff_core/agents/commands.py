from enum import Enum


class Command(str, Enum):
    STATUS = "status"
    REPORT = "report"
    RESET = "reset"

    CLIENT_INTAKE = "client_intake"
    SCHEDULE_MEETING = "schedule_meeting"
    SEND_FOLLOW_UP = "send_follow_up"
    SUMMARIZE = "summarize"


ALL_COMMANDS = {c.value for c in Command}

