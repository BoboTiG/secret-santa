from secret_santa.emails import generate_message, get_person
from secret_santa.utils import load_data


def check(email: str) -> None:
    assert "{{" not in email
    assert "}}" not in email
    assert "\n\n\n" not in email


def test_generate_message(data):
    event, people = load_data(data)
    assert len(people) > 1

    santa = people[0]
    buddy = people[1]
    santa.buddy = buddy.name

    email = generate_message(event, people, santa)
    check(email)
    assert email.count(santa.nature.title()) == 1
    assert email.count(santa.name) == 1
    assert email.count(buddy.name) == 1

    buddy.wishes = ["livre"]
    email = generate_message(event, people, santa)
    check(email)
    assert "    - livre" in email

    buddy.wishes = ["livre", "poupée gonflable"]
    email = generate_message(event, people, santa)
    check(email)
    assert "    - livre\n    - poupée gonflable" in email


def test_get_person(alice, bob):
    people = []
    assert not get_person(people, "Alice")

    people.append(alice)
    assert get_person(people, "Alice") == alice

    people.append(bob)
    assert get_person(people, "Bob") == bob
