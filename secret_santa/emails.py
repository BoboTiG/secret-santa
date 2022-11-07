import os
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from time import sleep
from typing import Callable, Dict, Tuple, Type

from jinja2 import Template

from .constants import INIT_EVENT_DESC
from .models import Event, People, Person


def get_person(people: People, name: str) -> Person:
    return next((person for person in people.values() if person.name == name))


def generate_message(
    body: str,
    subject: str,
    sender: Address,
    recipient: Person,
) -> EmailMessage:
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["Errors-To"] = msg["From"]
    msg["Disposition-Notification-To"] = msg["From"]  # For read receipt
    msg["To"] = Address(recipient.name, *recipient.email.split("@"))
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


def init_msg(event: Event, people: People, santa: Person) -> str:
    template = Template(source=INIT_EVENT_DESC)
    return template.render(santa=santa, event=event)


def results_msg(event: Event, people: People, santa: Person) -> str:
    buddy = get_person(people, santa.buddy)
    template = Template(source=event.description)
    return template.render(santa=santa, buddy=buddy)


def send_emails(
    event: Event,
    people: People,
    sleep_sec: float = 1.0,
    smtp_cls: Type[smtplib.SMTP] = smtplib.SMTP_SSL,
    msg_body_fn: Callable = results_msg,
) -> None:
    hostname, username, password = get_smtp_details(dict(**os.environ))
    sender = Address(event.sender, *event.email.split("@"))

    with smtp_cls(host=hostname) as server:
        server.login(username, password)

        for person in people.values():
            body = msg_body_fn(event, people, person)
            msg = generate_message(body, event.name, sender, person)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
            sleep(sleep_sec)
