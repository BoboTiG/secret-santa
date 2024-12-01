from pathlib import Path

import pytest

from secret_santa.models import Event, Person
from secret_santa.utils import load_data


@pytest.mark.parametrize("name", ["Name", ""])
@pytest.mark.parametrize("description", ["Description", ""])
@pytest.mark.parametrize("manager_email_name", ["Sender", ""])
@pytest.mark.parametrize("manager_email_id", ["Email", ""])
@pytest.mark.parametrize("kickoff_email_title", ["Title", ""])
@pytest.mark.parametrize("kickoff_email_body", ["Body", ""])
def test_event_empty_mandatory_field(  # noqa: PLR0913
    name: str,
    description: str,
    manager_email_name: str,
    manager_email_id: str,
    kickoff_email_title: str,
    kickoff_email_body: str,
) -> None:
    if all((name, description, manager_email_name, manager_email_id)):
        pytest.skip()
    with pytest.raises(ValueError, match=r".* is missing the .*"):
        Event(name, description, manager_email_name, manager_email_id, kickoff_email_title, kickoff_email_body)


def test_event_invalid_email() -> None:
    with pytest.raises(ValueError, match="Invalid 'email': 'bad-email'"):
        Event("Name", "Description", "Sender", "bad-email", "Title", "Body")


def test_event(opened_event: Path) -> None:
    event, _ = load_data(opened_event)
    assert event.hash == "2060b270cac877603cb581501514a036174551a63ea29d13f6b0092a84f6df7e"
    print(event.asdict())
    assert event.asdict() == {
        "name": "[2022] Noël au moulin !",
        "description": "Salut {{ santa.nature.title() }} Noël {{ santa.name }} !\n\nJ’ai l’honneur de te dévoiler que tu pourras faire plaisir à {{ santa.buddy }} pour Noël {{ '🎅' if santa.nature == 'papa' else '🤶' }}\n{%if buddy.wishes %}\nÀ titre d’information, {{ 'il' if buddy.nature == 'papa' else 'elle' }} ne serait pas contre un{{ ' (ou plusieurs)' if buddy.wishes|length > 1 else '' }} cadeau de cette liste :\n{% for wish in buddy.wishes: %}\n    - {{ wish }}\n{%- endfor %}\n\nBien entendu, libre à toi de suivre cette liste ou non.\n{% endif %}\nBonne chasse aux cadeaux, et ne perd pas un rein dans l’histoire : l’important est de prendre du bon temps entre nous ❤\n\nLa bise 💋\n",
        "manager_email_name": "Zed",
        "manager_email_id": "zed@localhost",
        "kickoff_email_title": "🌠 Top départ ! {}",
        "kickoff_email_body": "Salutations {{ santa.nature.title() }} Noël {{ santa.name }} !\n\nC’est le début des hostilités, et je t’invite à aller sur cette page pour remplir ta liste des souhaits : https://secret-santa.example.org/{{ event.hash }}/{{ santa.hash }}\n\nLa suite début décembre,\nLa bise 💋\n",
    }


@pytest.mark.parametrize("name", ["Name", ""])
@pytest.mark.parametrize("nature", ["nature", ""])
@pytest.mark.parametrize("email", ["Email", ""])
def test_person_empty_mandatory_field(name: str, nature: str, email: str) -> None:
    if all((name, nature, email)):
        pytest.skip()
    with pytest.raises(ValueError, match=r".* is missing the .*"):
        Person(name, nature, email, [], "")


def test_person_invalid_email() -> None:
    with pytest.raises(ValueError, match="Invalid 'email': 'bad-email'"):
        Person("Alice", "maman", "bad-email", [], "")


def test_person_invalid_nature() -> None:
    with pytest.raises(ValueError, match="Invalid 'nature': 'alien'"):
        Person("Alien", "alien", "a@b.c", [], "")


def test_person(alice: Person) -> None:
    assert alice.hash == "0763ff544f5af8bbbabf528f6f109b64c25fc099b4520a7fcc527a8a7be47746"
    assert alice.asdict() == {
        "nature": "maman",
        "email": "alice@localhost",
        "wishes": [],
        "buddy": None,
    }
