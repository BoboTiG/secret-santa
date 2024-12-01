from pathlib import Path

from secret_santa.models import Event, Person
from secret_santa.utils import create_init_emails, create_results_emails, load_data


def check(body: str) -> None:
    assert "{" not in body
    assert "}" not in body
    assert "\n\n\n" not in body


def test_create_init_emails(alice: Person, bob: Person, ended_event: Path) -> None:
    event, people = load_data(ended_event)

    messages = create_init_emails(event, people)
    for message in messages:
        body = message.get_content()
        check(body)

        assert message["Subject"] == "🌠 Top départ ! [2021] Noël au moulin !"

        if alice.name in message["To"]:
            assert "Salutations Maman Noël Alice !" in body
            assert f"/{event.hash}/{alice.hash}" in body
        else:
            assert "Salutations Papa Noël Bob !" in body
            assert f"/{event.hash}/{bob.hash}" in body


def test_create_results_emails(alice: Person, bob: Person, ended_event: Path) -> None:
    event, people = load_data(ended_event)

    people[bob.name].wishes = ["livre", "poupée gonflable"]

    messages = create_results_emails(event, people)
    for message in messages:
        body = message.get_content()
        check(body)

        assert message["Subject"] == "[2021] Noël au moulin !"

        assert body.count(alice.name) == 1
        assert body.count(bob.name) == 1

        if alice.name in message["To"]:
            assert "🤶" in body
            assert "🎅" not in body
            assert body.count(alice.nature.title()) == 1
            assert "À titre d’information" in body
            assert "    - livre\n    - poupée gonflable" in body
        else:
            assert "🤶" not in body
            assert "🎅" in body
            assert body.count(bob.nature.title()) == 1
            assert "À titre d’information" not in body


def test_load_data(opened_event: Path) -> None:
    event, people = load_data(opened_event)
    assert isinstance(event, Event)
    assert isinstance(people, dict)
    assert isinstance(people["Alice"], Person)
