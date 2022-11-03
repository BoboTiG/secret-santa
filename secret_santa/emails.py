from email.message import EmailMessage

from .models import Event, People, Person


def get_person(people: People, name: str) -> Person | None:
    return next((person for person in people if person.name == name), None)


def generate_message(event: Event, santa: Person, buddy: Person) -> EmailMessage:
    from email.headerregistry import Address
    from email.utils import make_msgid

    from jinja2 import Template

    template = Template(source=event.description)
    body = template.render(santa=santa, buddy=buddy)

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = event.name
    msg["From"] = Address(event.sender, *event.email.split("@"))
    msg["Errors-To"] = event.email
    msg["To"] = Address(santa.name, *santa.email.split("@"))
    msg["Message-ID"] = make_msgid()
    return msg


def get_smtp_password() -> str:
    from getpass import getpass

    return getpass("SMTP password: ").strip()


def get_smtp_details():
    import os

    environ = os.environ
    hostname = environ.get("SS_SMTP_HOSTNAME") or input("SMTP hostname: ").strip()
    username = environ.get("SS_SMTP_USERNAME") or input("SMTP username: ").strip()
    password = environ.get("SS_SMTP_PASSWORD") or get_smtp_password()
    return hostname, username, password


def send_emails(event: Event, people: People) -> None:
    hostname, username, password = get_smtp_details()
    import smtplib
    from time import sleep

    with smtplib.SMTP_SSL(hostname) as server:
        server.login(username, password)
        for santa in people:
            buddy = get_person(people, santa.buddy)
            msg = generate_message(event, santa, buddy)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
            sleep(1)
