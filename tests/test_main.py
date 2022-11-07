import smtplib
from unittest.mock import patch

from secret_santa import emails
from secret_santa.__main__ import main

ENV = {
    "SS_SMTP_HOSTNAME": "a",
    "SS_SMTP_USERNAME": "b",
    "SS_SMTP_PASSWORD": "c",
}


class CustomSMTP(smtplib.SMTP):
    def __init__(self, host="", **_):
        assert host == ENV["SS_SMTP_HOSTNAME"]
        super().__init__(local_hostname=host)

    def login(self, user, password):
        assert user == ENV["SS_SMTP_USERNAME"]
        assert password == ENV["SS_SMTP_PASSWORD"]

    def sendmail(self, from_addr, to_addrs, msg):
        assert from_addr
        assert to_addrs
        assert msg


def test_init(opened_event):
    send_emails_orig = emails.send_emails
    cli_args = ["init", "--event", str(opened_event)]

    def send_emails(*args, **kwargs):
        return send_emails_orig(*args, **kwargs, sleep_sec=0.0, smtp_cls=CustomSMTP)

    # First run
    with (
        patch("secret_santa.emails.send_emails", send_emails),
        patch("os.environ", ENV),
    ):
        assert main(cli_args) == 0

    def true(*_):
        return True

    # Second run
    with patch("secret_santa.__main__.has_ended", true):
        assert main(cli_args) == 1


def test_results(opened_event, capsys):
    send_emails_orig = emails.send_emails
    cli_args = ["results", "--event", str(opened_event)]

    def send_emails(*args):
        return send_emails_orig(*args, sleep_sec=0.0, smtp_cls=CustomSMTP)

    # First run
    with (
        patch("secret_santa.emails.send_emails", send_emails),
        patch("os.environ", ENV),
    ):
        assert main(cli_args) == 0
        out, _ = capsys.readouterr()
        assert "Les résultats sont déjà connus" not in out

    # Second run
    assert main(cli_args) == 1
    out, _ = capsys.readouterr()
    assert "Les résultats sont déjà connus" in out


def test_front():
    cli_args = ["front"]

    def serve(*_):
        return 0

    with (patch("secret_santa.server.serve", serve)):
        assert main(cli_args) == 0
