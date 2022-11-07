from unittest.mock import patch

import pytest

from secret_santa import picker
from secret_santa.exceptions import BadDraw, NotEnoughPeople
from secret_santa.models import Person


def test_pick_a_buddy(alice, bob):
    with pytest.raises(NotEnoughPeople):
        picker.pick_a_buddy([], alice)

    with pytest.raises(BadDraw):
        picker.pick_a_buddy([alice], alice)

    assert picker.pick_a_buddy([alice, bob], alice) == bob


def test_pick_names(alice, bob):
    people = []
    with pytest.raises(NotEnoughPeople):
        picker.pick_names(people)

    people.append(alice)
    with pytest.raises(NotEnoughPeople):
        picker.pick_names(people)

    people.append(bob)
    secret = picker.pick_names(people)
    assert len(secret) == 2
    assert alice in secret
    assert secret[0].buddy == bob.name
    assert bob in secret
    assert secret[1].buddy == alice.name


def test_picker_bad_draw(alice, bob, capsys):
    draw_orig = picker.draw
    count = 0

    def bad_draw(*args):
        nonlocal count
        count += 1
        if count == 1:
            raise BadDraw()
        return draw_orig(*args)

    with patch("secret_santa.picker.draw", bad_draw):
        secret_santas = picker.pick_names([alice, bob])
        assert isinstance(secret_santas, list)
        assert len(secret_santas) == 2
        assert isinstance(secret_santas[0], Person)
        assert isinstance(secret_santas[1], Person)

    out, _ = capsys.readouterr()
    assert out.count(" !! Invalid draw, new attempt … ") == 1
