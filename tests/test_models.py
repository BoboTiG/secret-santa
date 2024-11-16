from pathlib import Path

import pytest

from secret_santa.models import Event, Person
from secret_santa.utils import load_data


@pytest.mark.parametrize("name", ["Name", ""])
@pytest.mark.parametrize("description", ["Description", ""])
@pytest.mark.parametrize("sender", ["Sender", ""])
@pytest.mark.parametrize("email", ["Email", ""])
def test_event_empty_mandatory_field(name: str, description: str, sender: str, email: str) -> None:
    if all((name, description, sender, email)):
        pytest.skip()
    with pytest.raises(ValueError, match=r".* is missing the .*"):
        Event(name, description, sender, email)


def test_event_invalid_email() -> None:
    with pytest.raises(ValueError, match="Invalid 'email': 'bad-email'"):
        Event("Name", "Description", "Sender", "bad-email")


def test_event(opened_event: Path) -> None:
    event, _ = load_data(opened_event)
    assert event.hash == "2060b270cac877603cb581501514a036174551a63ea29d13f6b0092a84f6df7e"
    print(event.asdict())
    assert event.asdict() == {
        "name": "[2022] Noël au moulin !",
        "description": "Salut {{ santa.nature.title() }} Noël {{ santa.name }} !\n\nJ’ai l’honneur de te dévoiler que tu pourras faire plaisir à {{ santa.buddy }} pour Noël {{ '🎅' if santa.nature == 'papa' else '🤶' }}\n{%if buddy.wishes %}\nÀ titre d’information, {{ 'il' if buddy.nature == 'papa' else 'elle' }} ne serait pas contre un{{ ' (ou plusieurs)' if buddy.wishes|length > 1 else '' }} cadeau de cette liste :\n{% for wish in buddy.wishes: %}\n    - {{ wish }}\n{%- endfor %}\n\nBien entendu, libre à toi de suivre cette liste ou non.\n{% endif %}\nBonne chasse aux cadeaux, et ne perd pas un rein dans l’histoire : l’important est de prendre du bon temps entre nous ❤\n\nLa bise 💋\n",
        "sender": "Zed",
        "email": "zed@localhost",
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
