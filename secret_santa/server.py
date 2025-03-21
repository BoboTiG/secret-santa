"""
Simple webserver for the frontend.
"""

from __future__ import annotations

from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING

from bottle import redirect, request, route, run, static_file, template

from secret_santa.utils import load_data, save_results

if TYPE_CHECKING:
    from secret_santa.models import Event, Person

ROOT = Path(__file__).parent
EVENTS = ROOT.parent / "events"
STATIC = ROOT / "static"


def get_person(
    event_hash: str, person_hash: str, events_folder: Path = EVENTS
) -> tuple[Path | None, Event | None, Person | None]:
    for data in events_folder.glob("*/event.yml"):
        event, people = load_data(data.parent)
        if event.hash != event_hash:
            continue

        # Results are known, meaning the event is closed
        if any(person.buddy for person in people.values()):
            continue

        return (
            data.parent,
            event,
            next((p for p in people.values() if p.hash == person_hash), None),
        )

    return None, None, None


@route("/static/<file:path>", method=["GET"])
def static(file: str) -> str:
    return static_file(file, STATIC)


@route("/", method=["GET"])
def homepage() -> str:
    sleep(1)  # Cooldown

    return template("index.html", template_lookup=[STATIC])


@route("/<event_hash>/<person_hash>", method=["GET", "POST"])
def profile(event_hash: str, person_hash: str, events_folder: Path = EVENTS) -> None:
    """
    GET: show profile
    POST: update wishes list, then show updated profile
    """
    sleep(1)  # Cooldown

    folder, event, person = get_person(event_hash, person_hash, events_folder=events_folder)
    if not person:
        return redirect("/")

    # For Mypy
    assert folder  # noqa: S101
    assert event  # noqa: S101
    assert person  # noqa: S101

    if request.method == "POST":
        wishes: list[str] = list(
            filter(
                None,
                (request.forms.getunicode(f"wish-{idx}", encoding="utf-8") for idx in range(3)),
            )
        )
        for idx in range(len(wishes)):
            wishes[idx] = wishes[idx].strip()
        if wishes != person.wishes:
            print(f">>> {person.name} wishes: {person.wishes} → {wishes}", flush=True)
            _, people = load_data(folder)
            person.wishes = wishes
            people[person.name] = person
            save_results(folder, people)
        return redirect(f"/{event_hash}/{person_hash}")

    return template("buddy.html", template_lookup=[STATIC], event=event, person=person)


def serve() -> int:  # pragma: nocover
    port = sum(ord(c) for c in "Secret Santa!")  # 1182
    run(host="0.0.0.0", port=port)  # noqa: S104
    return 0
