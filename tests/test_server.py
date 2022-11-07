from pathlib import Path

import pytest
from boddle import boddle
from bottle import HTTPResponse

from secret_santa.server import homepage, profile, static
from secret_santa.utils import load_data


def test_homepage():
    with boddle():
        html = homepage()
    assert "<b>Ou</b> alors, l’événement est terminé" in html


def test_profile_incorrect_event(opened_event: Path):
    with (
        boddle(method="get", path="/event_hash/person_hash"),
        pytest.raises(HTTPResponse),
    ):
        profile("event_hash", "person_hash", events_folder=opened_event.parent)


def test_profile_incorrect_person(opened_event: Path):
    event, _ = load_data(opened_event)
    with (
        boddle(method="get", path=f"/{event.hash}/person_hash"),
        pytest.raises(HTTPResponse),
    ):
        profile(event.hash, "person_hash", events_folder=opened_event.parent)


def test_profile_ended_event(ended_event: Path):
    event, people = load_data(ended_event)
    person = people["Alice"]
    with (
        boddle(method="get", path=f"/{event.hash}/{person.hash}"),
        pytest.raises(HTTPResponse),
    ):
        profile(event.hash, person.hash, events_folder=ended_event.parent)


def test_profile_show(opened_event: Path):
    event, people = load_data(opened_event)
    person = people["Alice"]
    with boddle(method="get", path=f"/{event.hash}/{person.hash}"):
        html = profile(event.hash, person.hash, events_folder=opened_event.parent)
    assert "<b>Alice</b>, bienvenue sur ta page perso" in html


def test_profile_update(opened_event: Path):
    event, people = load_data(opened_event)
    person = people["Alice"]

    # Pre-check
    with boddle(method="get", path=f"/{event.hash}/{person.hash}"):
        html = profile(event.hash, person.hash, events_folder=opened_event.parent)
    assert 'name="wish-0" value=""' in html
    assert 'name="wish-1" value=""' in html
    assert 'name="wish-2" value=""' in html

    with (
        boddle(
            method="post",
            path=f"/{event.hash}/{person.hash}",
            params={
                "wish-0": "un livre de SF",
                "wish-2": "un ticket de métro",
            },
        ),
        pytest.raises(HTTPResponse),
    ):
        profile(event.hash, person.hash, events_folder=opened_event.parent)

    # Check
    with boddle(method="get", path=f"/{event.hash}/{person.hash}"):
        html = profile(event.hash, person.hash, events_folder=opened_event.parent)
    assert 'name="wish-0" value="un livre de SF"' in html
    assert 'name="wish-1" value="un ticket de métro"' in html
    assert 'name="wish-2" value=""' in html


def test_static():
    with boddle(method="get", params={"file": "style.css"}):
        response = static("style.css")
    assert response.status_code == 200
