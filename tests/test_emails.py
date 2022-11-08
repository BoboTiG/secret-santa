from unittest.mock import patch

from secret_santa import emails


def test_get_smtp_password():
    def getpass(*_):
        return "  azerty   "

    with patch("getpass.getpass", getpass):
        assert emails.get_smtp_password() == "azerty"


def test_get_smtp_details():
    environs = {
        "SS_SMTP_HOSTNAME": "a",
        "SS_SMTP_USERNAME": "b",
        "SS_SMTP_PASSWORD": "c",
    }
    assert emails.get_smtp_details(environs) == ("a", "b", "c")
