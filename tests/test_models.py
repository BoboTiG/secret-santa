import pytest

from secret_santa.models import Event, Person
from secret_santa.utils import load_data


@pytest.mark.parametrize("name", ["Name", ""])
@pytest.mark.parametrize("description", ["Description", ""])
@pytest.mark.parametrize("sender", ["Sender", ""])
@pytest.mark.parametrize("email", ["Email", ""])
def test_event_empty_mandatory_field(name, description, sender, email):
    if all((name, description, sender, email)):
        pytest.skip()
    with pytest.raises(ValueError, match=r".* is missing the .*"):
        Event(name, description, sender, email)


def test_event_invalid_email():
    with pytest.raises(ValueError, match="Invalid 'email': 'bad-email'"):
        Event("Name", "Description", "Sender", "bad-email")


def test_event(opened_event):
    event, _ = load_data(opened_event)
    assert event.hash == "535f21c27359fa17b18f804915ceef3c"
    print(event.asdict())
    assert event.asdict() == {
        "name": "[2022] Noël au moulin !",
        "description": "Salut {{ santa.nature.title() }} Noël {{ santa.name }} !\n\nJ’ai l’honneur de te dévoiler que tu pourras faire plaisir à {{ santa.buddy }} pour Noël {{ '🎅' if santa.nature == 'papa' else '🤶' }}\n{%if buddy.wishes %}\nÀ titre d’information, {{ 'il' if buddy.nature == 'papa' else 'elle' }} ne serait pas contre un{{ ' (ou plusieurs)' if buddy.wishes|length > 1 else '' }} cadeau de cette liste :\n{% for wish in buddy.wishes: %}\n    - {{ wish }}\n{%- endfor %}\n\nBien entendu, libre à toi de suivre cette liste ou non.\n{% endif %}\nBonne chasse aux cadeaux, et ne perd pas un rein dans l’histoire : l’important est de prendre du bon temps entre nous ❤\n\nLa bise 💋\n",  # noqa
        "sender": "Zed",
        "email": "zed@localhost",
    }


@pytest.mark.parametrize("name", ["Name", ""])
@pytest.mark.parametrize("nature", ["nature", ""])
@pytest.mark.parametrize("email", ["Email", ""])
def test_person_empty_mandatory_field(name, nature, email):
    if all((name, nature, email)):
        pytest.skip()
    with pytest.raises(ValueError, match=r".* is missing the .*"):
        Person(name, nature, email, [], "")


def test_person_invalid_email():
    with pytest.raises(ValueError, match="Invalid 'email': 'bad-email'"):
        Person("Alice", "maman", "bad-email", [], "")


def test_person_invalid_nature():
    with pytest.raises(ValueError, match="Invalid 'nature': 'alien'"):
        Person("Alien", "alien", "a@b.c", [], "")


def test_person(alice: Person):
    assert alice.hash == "73b8e2633509d29c74d928be2cefb6eb"
    assert alice.asdict() == {
        "nature": "maman",
        "email": "alice@localhost",
        "wishes": [],
        "buddy": None,
    }
