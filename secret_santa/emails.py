import os
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from time import sleep
from typing import Dict, Tuple, Type

from jinja2 import Template

from .models import Event, People, Person


def get_person(people: People, name: str) -> Person:
    return next((person for person in people if person.name == name))


def generate_message(event: Event, santa: Person, buddy: Person) -> EmailMessage:
    template = Template(source=event.description)
    body = template.render(santa=santa, buddy=buddy)

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = event.name
    msg["From"] = Address(event.sender, *event.email.split("@"))
    msg["Errors-To"] = msg["From"]
    msg["Disposition-Notification-To"] = msg["From"]  # For read receipt
    msg["To"] = Address(santa.name, *santa.email.split("@"))
    msg["Message-ID"] = make_msgid()
    return msg


def get_smtp_password() -> str:
    from getpass import getpass

    return getpass("SMTP password: ").strip()


def get_smtp_details(
    environs: Dict[str, str]
) -> Tuple[str, str, str]:  # pragma: nocover
    hostname = environs.get("SS_SMTP_HOSTNAME") or input("SMTP hostname: ").strip()
    username = environs.get("SS_SMTP_USERNAME") or input("SMTP username: ").strip()
    password = environs.get("SS_SMTP_PASSWORD") or get_smtp_password()
    return hostname, username, password


def send_emails(
    event: Event,
    people: People,
    sleep_sec: float = 1.0,
    smtp_cls: Type[smtplib.SMTP] = smtplib.SMTP_SSL,
) -> None:
    hostname, username, password = get_smtp_details(dict(**os.environ))

    with smtp_cls(host=hostname) as server:
        server.login(username, password)
        for santa in people:
            buddy = get_person(people, santa.buddy)
            msg = generate_message(event, santa, buddy)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
            sleep(sleep_sec)
