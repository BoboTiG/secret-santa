from __future__ import annotations

from email.headerregistry import Address
from typing import TYPE_CHECKING

from jinja2 import Template

from secret_santa.constants import INIT_EVENT_DESC, INIT_EVENT_NAME
from secret_santa.emails import generate_message
from secret_santa.models import Event, People, Person

if TYPE_CHECKING:
    from email.message import EmailMessage
    from pathlib import Path


def create_init_emails(event: Event, people: People) -> list[EmailMessage]:
    template = Template(source=INIT_EVENT_DESC)
    subject = INIT_EVENT_NAME.format(event.name)
    sender = Address(event.sender, *event.email.split("@"))
    messages: list[EmailMessage] = []

    for santa in people.values():
        body = template.render(santa=santa, event=event)
        recipient = Address(santa.name, *santa.email.split("@"))
        message = generate_message(subject, body, sender, recipient)
        messages.append(message)

    return messages


def create_results_emails(event: Event, people: People) -> list[EmailMessage]:
    template = Template(source=event.description)
    subject = event.name
    sender = Address(event.sender, *event.email.split("@"))
    messages: list[EmailMessage] = []

    for santa in people.values():
        buddy = next(p for p in people.values() if p.name == santa.buddy)
        body = template.render(santa=santa, buddy=buddy)
        recipient = Address(santa.name, *santa.email.split("@"))
        message = generate_message(subject, body, sender, recipient)
        messages.append(message)

    return messages


def load_data(folder: Path) -> tuple[Event, People]:
    from yaml import safe_load

    with (folder / "event.yml").open(encoding="utf-8") as fh:
        event = Event(**safe_load(fh))
    with (folder / "people.yml").open(encoding="utf-8") as fh:
        people = {name: Person(name, **details) for name, details in safe_load(fh).items()}
    return event, people


def save_results(folder: Path, people: People) -> None:
    from yaml import safe_dump

    data = {name: person.asdict() for name, person in people.items()}
    file = folder / "people.yml"
    with file.open(mode="w", encoding="utf-8") as fh:
        safe_dump(data, fh, allow_unicode=True, encoding="utf-8", sort_keys=False)
