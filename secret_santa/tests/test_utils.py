from secret_santa.models import Event, Person
from secret_santa.utils import load_data


def test_load_data(data):
    event, people = load_data(data)
    assert isinstance(event, Event)
    assert isinstance(people, list)
    assert isinstance(people[0], Person)
