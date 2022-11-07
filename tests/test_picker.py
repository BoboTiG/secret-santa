from unittest.mock import patch

import pytest

from secret_santa import picker
from secret_santa.exceptions import BadDraw, NotEnoughPeople
from secret_santa.models import Person


def test_pick_a_buddy(alice: Person, bob: Person):
    people = {}
    with pytest.raises(NotEnoughPeople):
        picker.pick_a_buddy(people, alice)

    people[alice.name] = alice
    with pytest.raises(BadDraw):
        picker.pick_a_buddy(people, alice)

    people[bob.name] = bob
    assert picker.pick_a_buddy(people, alice) == bob


def test_pick_names(alice: Person, bob: Person):
    people = {}
    with pytest.raises(NotEnoughPeople):
        picker.pick_names(people)

    people[alice.name] = alice
    with pytest.raises(NotEnoughPeople):
        picker.pick_names(people)

    people[bob.name] = bob
    secret = picker.pick_names(people)
    assert len(secret.keys()) == 2
    assert alice.name in secret
    assert secret[alice.name].buddy == bob.name
    assert bob.name in secret
    assert secret[bob.name].buddy == alice.name


def test_picker_bad_draw(alice: Person, bob: Person, capsys):
    draw_orig = picker.draw
    count = 0
    people = {
        alice.name: alice,
        bob.name: bob,
    }

    def bad_draw(*args):
        nonlocal count
        count += 1
        if count == 1:
            raise BadDraw()
        return draw_orig(*args)

    with patch("secret_santa.picker.draw", bad_draw):
        secret_santas = picker.pick_names(people)
        assert isinstance(secret_santas, dict)
        assert len(secret_santas.keys()) == 2
        for name, santa in secret_santas.items():
            assert isinstance(name, str)
            assert isinstance(santa, Person)

    out, _ = capsys.readouterr()
    assert out.count(" !! Invalid draw, new attempt … ") == 1
