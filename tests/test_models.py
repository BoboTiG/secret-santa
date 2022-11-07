import pytest

from secret_santa.models import Event, Person


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
