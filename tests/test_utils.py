from secret_santa.models import Event, Person
from secret_santa.utils import hash_buddy, hash_event, load_data


def test_buddy_hash(alice):
    assert hash_buddy(alice) == "f3fc2e3b8b7fc0fde5af2c2ad30a549f"


def test_hash_event(data):
    event, _ = load_data(data)
    assert hash_event(event.name) == "0736d59f132cab63469364228a6d123f"


def test_load_data(data):
    event, people = load_data(data)
    assert isinstance(event, Event)
    assert isinstance(people, list)
    assert isinstance(people[0], Person)
