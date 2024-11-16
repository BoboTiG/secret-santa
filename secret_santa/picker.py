from __future__ import annotations

from typing import TYPE_CHECKING

from secret_santa.exceptions import BadDrawError, NotEnoughPeopleError

if TYPE_CHECKING:
    from secret_santa.models import People, Person


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
        raise NotEnoughPeopleError

    people = {name: person for name, person in people.items() if name != santa.name}
    if not people:
        raise BadDrawError

    from random import choice

    return choice(list(people.values()))  # noqa: S311


def pick_names(people: People) -> People:
    if len(people.keys()) < 2:
        raise NotEnoughPeopleError

    while "picking":
        try:
            return draw(people)
        except BadDrawError:  # noqa: PERF203
            print(" !! Invalid draw, new attempt … ")

    raise RuntimeError
