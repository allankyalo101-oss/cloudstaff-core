from typing import Dict, Set


STATE_TRANSITIONS: Dict[str, Set[str]] = {
    "idle": {
        "client_intake",
        "status",
        "report",
        "reset",
    },
    "intake_completed": {
        "schedule_meeting",
        "status",
        "report",
        "reset",
    },
    "meeting_scheduled": {
        "send_follow_up",
        "status",
        "report",
        "reset",
    },
    "follow_up_sent": {
        "status",
        "report",
        "reset",
    },
}

