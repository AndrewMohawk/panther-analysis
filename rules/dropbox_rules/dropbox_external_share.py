import json
from unittest.mock import MagicMock

from panther_base_helpers import deep_get

ALLOWED_DOMAINS = [
    # "example.com"
]


def rule(event):
    global ALLOWED_DOMAINS  # pylint: disable=global-statement
    if isinstance(ALLOWED_DOMAINS, MagicMock):
        ALLOWED_DOMAINS = set(json.loads(ALLOWED_DOMAINS()))  # pylint: disable=not-callable
    if deep_get(event, "event_type", "_tag", default="") == "shared_content_add_member":
        participants = event.get("participants", [{}])
        for participant in participants:
            email = participant.get("user", {}).get("email", "")
            if email.split("@")[-1] not in ALLOWED_DOMAINS:
                return True
    return False


def title(event):
    actor = deep_get(event, "actor", "user", "email", default="<ACTOR_NOT_FOUND>")
    assets = [e.get("display_name", "") for e in event.get("assets", [{}])]
    participants = event.get("participants", [{}])
    external_participants = []
    for participant in participants:
        email = participant.get("user", {}).get("email", "")
        if email.split("@")[-1] not in ALLOWED_DOMAINS:
            external_participants.append(email)
    return f"Dropbox: [{actor}] shared [{assets}] with external user [{external_participants}]."


def alert_context(event):
    external_participants = []
    participants = event.get("participants", [{}])
    for participant in participants:
        email = participant.get("user", {}).get("email", "")
        if email.split("@")[-1] not in ALLOWED_DOMAINS:
            external_participants.append(email)
    return {"external_participants": external_participants}
