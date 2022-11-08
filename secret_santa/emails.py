import os
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from time import sleep
from typing import Dict, List, Tuple, Type


def generate_message(
    subject: str, body: str, sender: Address, recipient: Address
) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["Errors-To"] = msg["From"]
    msg["Disposition-Notification-To"] = msg["From"]  # For read receipt
    msg["To"] = recipient
    msg["Message-ID"] = make_msgid()
    msg.set_content(body)
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
    messages: List[EmailMessage],
    smtp_cls: Type[smtplib.SMTP] = smtplib.SMTP_SSL,
    sleep_sec: float = 1.0,
) -> None:
    hostname, username, password = get_smtp_details(dict(**os.environ))
    with smtp_cls(host=hostname) as server:
        server.login(username, password)
        for message in messages:
            server.sendmail(message["From"], message["To"], message.as_string())
            sleep(sleep_sec)
