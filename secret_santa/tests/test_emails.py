from secret_santa.emails import generate_message, get_person
from secret_santa.utils import load_data


def check(email: str) -> None:
    assert "{{" not in email
    assert "}}" not in email
    assert "\n\n\n" not in email


def test_generate_message(data):
    event, people = load_data(data)
    assert len(people) > 1

    santa, buddy = people
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
    assert "    - livre" in email.get_content()

    buddy.wishes = ["livre", "poupée gonflable"]
    email = generate_message(event, santa, buddy)
    check(email)
    assert "    - livre\n    - poupée gonflable" in email.get_content()


def test_get_person(alice, bob):
    people = [alice]
    assert get_person(people, "Alice") == alice

    people.append(bob)
    assert get_person(people, "Bob") == bob
