from __future__ import annotations

import smtplib
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

from secret_santa import emails
from secret_santa.__main__ import main

if TYPE_CHECKING:
    from email.message import EmailMessage
    from pathlib import Path

    import pytest

ENV = {
    "SS_SMTP_HOSTNAME": "a",
    "SS_SMTP_USERNAME": "b",
    "SS_SMTP_PASSWORD": "c",
}


class CustomSMTP(smtplib.SMTP_SSL):
    def __init__(self, *, host: str = "", **_: dict[str, Any]) -> None:
        assert host == ENV["SS_SMTP_HOSTNAME"]
        super().__init__(local_hostname=host)

    def login(self, user: str, password: str) -> None:
        assert user == ENV["SS_SMTP_USERNAME"]
        assert password == ENV["SS_SMTP_PASSWORD"]

    def sendmail(self, from_addr: str, to_addrs: str, msg: Any) -> None:
        assert from_addr
        assert to_addrs
        assert msg


def test_init(opened_event: Path) -> None:
    send_emails_orig = emails.send_emails
    cli_args = ["init", "--event", str(opened_event)]

    def send_emails(
        messages: list[EmailMessage],
        *,
        smtp_cls: type[smtplib.SMTP_SSL] = smtplib.SMTP_SSL,  # noqa: ARG001
        sleep_sec: float = 1.0,  # noqa: ARG001
        conn: smtplib.SMTP_SSL | None = None,
    ) -> None:
        return send_emails_orig(messages, conn=conn, sleep_sec=0.0, smtp_cls=CustomSMTP)

    # First run
    with (
        patch("secret_santa.emails.send_emails", send_emails),
        patch("os.environ", ENV),
    ):
        assert main(cli_args) == 0

    # Second run
    with patch("secret_santa.__main__.has_ended", lambda *_: True):
        assert main(cli_args) == 1


def test_results(opened_event: Path, capsys: pytest.CaptureFixture) -> None:
    send_emails_orig = emails.send_emails
    smtp_connexion_orig = emails.smtp_connexion
    cli_args = ["results", "--event", str(opened_event)]

    def smtp_connexion() -> smtplib.SMTP_SSL:
        return smtp_connexion_orig(smtp_cls=CustomSMTP)

    def send_emails(
        messages: list[EmailMessage],
        *,
        smtp_cls: type[smtplib.SMTP_SSL] = smtplib.SMTP_SSL,  # noqa: ARG001
        sleep_sec: float = 1.0,  # noqa: ARG001
        conn: smtplib.SMTP_SSL | None = None,
    ) -> None:
        return send_emails_orig(messages, conn=conn, sleep_sec=0.0, smtp_cls=CustomSMTP)

    # First run
    with (
        patch("secret_santa.emails.send_emails", send_emails),
        patch("secret_santa.emails.smtp_connexion", smtp_connexion),
        patch("os.environ", ENV),
    ):
        assert main(cli_args) == 0
        out, _ = capsys.readouterr()
        assert "Les résultats sont déjà connus" not in out

    # Second run
    assert main(cli_args) == 1
    out, _ = capsys.readouterr()
    assert "Les résultats sont déjà connus" in out


def test_front() -> None:
    cli_args = ["front"]

    def serve() -> int:
        return 0

    with patch("secret_santa.server.serve", serve):
        assert main(cli_args) == 0
