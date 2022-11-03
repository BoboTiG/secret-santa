from .exceptions import BadDraw, NotEnoughPeople
from .models import People, Person


def draw(all_the_people: People) -> People:
    secret_santas = []
    people = all_the_people.copy()
    for santa in all_the_people:
        buddy = pick_a_buddy(people, santa)
        santa.buddy = buddy.name
        secret_santas.append(santa)
        people.remove(buddy)
    return secret_santas


def pick_a_buddy(people: People, santa: Person) -> Person:
    if not people:
        raise NotEnoughPeople()

    people = [person for person in people if person.name != santa.name]
    if not people:
        raise BadDraw()

    from random import choice

    return choice(people)


def pick_names(all_the_people: People) -> People:
    if len(all_the_people) < 2:
        raise NotEnoughPeople()

    while "picking":
        try:
            return draw(all_the_people)
        except BadDraw:
            print(" !! Invalid draw, new attempt ...")
    raise RuntimeError()
