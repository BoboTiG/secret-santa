import pytest
from secret_santa.exceptions import BadDraw, NotEnoughPeople
from secret_santa.picker import pick_a_buddy, pick_names


def test_pick_a_buddy(alice, bob):
    with pytest.raises(NotEnoughPeople):
        pick_a_buddy([], alice)

    with pytest.raises(BadDraw):
        pick_a_buddy([alice], alice)

    assert pick_a_buddy([alice, bob], alice) == bob


def test_pick_names(alice, bob):
    people = []
    with pytest.raises(NotEnoughPeople):
        pick_names(people)

    people.append(alice)
    with pytest.raises(NotEnoughPeople):
        pick_names(people)

    people.append(bob)
    secret = pick_names(people)
    assert len(secret) == 2
    assert alice in secret
    assert secret[0].buddy == bob.name
    assert bob in secret
    assert secret[1].buddy == alice.name
