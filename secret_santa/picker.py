from .exceptions import BadDraw, NotEnoughPeople
from .models import People, Person


def draw(all_the_people: People) -> People:
    secret_santas = {}
    people = all_the_people.copy()
    for santa in all_the_people.values():
        buddy = pick_a_buddy(people, santa)
        santa.buddy = buddy.name
        secret_santas[santa.name] = santa
        people.pop(buddy.name)
    return secret_santas


def pick_a_buddy(people: People, santa: Person) -> Person:
    if not people:
        raise NotEnoughPeople()

    people = {name: person for name, person in people.items() if name != santa.name}
    if not people:
        raise BadDraw()

    from random import choice

    return choice(list(people.values()))


def pick_names(people: People) -> People:
    if len(people.keys()) < 2:
        raise NotEnoughPeople()

    while "picking":
        try:
            return draw(people)
        except BadDraw:
            print(" !! Invalid draw, new attempt … ")

    raise RuntimeError()  # pragma:nocover
