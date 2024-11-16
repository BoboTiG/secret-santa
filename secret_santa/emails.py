from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from time import sleep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from email.headerregistry import Address


def generate_message(subject: str, body: str, sender: Address, recipient: Address) -> EmailMessage:
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


def get_smtp_details(environs: dict[str, str]) -> tuple[str, str, str]:
    hostname = environs.get("SS_SMTP_HOSTNAME") or input("SMTP hostname: ").strip()
    username = environs.get("SS_SMTP_USERNAME") or input("SMTP username: ").strip()
    password = environs.get("SS_SMTP_PASSWORD") or get_smtp_password()
    return hostname, username, password


def send_emails(
    messages: list[EmailMessage],
    *,
    smtp_cls: type[smtplib.SMTP_SSL] = smtplib.SMTP_SSL,
    sleep_sec: float = 1.0,
    conn: smtplib.SMTP_SSL | None = None,
) -> None:
    server = conn or smtp_connexion(smtp_cls=smtp_cls)
    for message in messages:
        server.sendmail(message["From"], message["To"], message.as_string())
        sleep(sleep_sec)
    server.close()


def smtp_connexion(*, smtp_cls: type[smtplib.SMTP_SSL] = smtplib.SMTP_SSL) -> smtplib.SMTP_SSL:
    hostname, username, password = get_smtp_details(dict(**os.environ))
    server = smtp_cls(host=hostname)
    server.login(username, password)
    return server
