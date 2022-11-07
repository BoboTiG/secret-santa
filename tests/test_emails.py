from unittest.mock import patch

from secret_santa import emails
from secret_santa.emails import generate_message, get_person
from secret_santa.models import Person
from secret_santa.utils import load_data


def check(email: str) -> None:
    assert "{{" not in email
    assert "}}" not in email
    assert "\n\n\n" not in email


def test_generate_message(alice: Person, bob: Person, ended_event):
    event, people = load_data(ended_event)
    assert len(people.keys()) > 1

    santa = people[alice.name]
    buddy = people[bob.name]
    santa.buddy = buddy.name

    email = generate_message(event, santa, buddy)
    check(email)
    body = email.get_content()
    assert "🤶" in body
    assert "🎅" not in body
    assert body.count(santa.nature.title()) == 1
    assert body.count(santa.name) == 1
    assert body.count(buddy.name) == 1

    buddy.wishes = ["livre"]
    email = generate_message(event, santa, buddy)
    check(email)
    body = email.get_content()
    assert "À titre d’information" in body
    assert "(ou plusieurs)" not in body
    assert "    - livre" in body

    buddy.wishes = ["livre", "poupée gonflable"]
    email = generate_message(event, santa, buddy)
    check(email)
    body = email.get_content()
    assert "(ou plusieurs)" in body
    assert "    - livre\n    - poupée gonflable" in body

    buddy.wishes = []
    email = generate_message(event, santa, buddy)
    check(email)
    assert "À titre d’information" not in email.get_content()


def test_get_person(alice: Person, bob: Person):
    people = {alice.name: alice}
    assert get_person(people, "Alice") == alice

    people[bob.name] = bob
    assert get_person(people, "Bob") == bob


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
