from secret_santa.models import Event, Person
from secret_santa.utils import load_data


def test_load_data(opened_event):
    event, people = load_data(opened_event)
    assert isinstance(event, Event)
    assert isinstance(people, dict)
    assert isinstance(people["Alice"], Person)
