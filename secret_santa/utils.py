from pathlib import Path
from typing import Tuple

from .models import Event, People, Person


def load_data(file: Path) -> Tuple[Event, People]:
    from yaml import safe_load

    with file.open(encoding="utf-8") as fh:
        raw = safe_load(fh)
    event = Event(**raw["event"])
    people = [Person(**person) for person in raw["people"].values()]
    return event, people


def result_file(file: Path) -> Path:
    return file.with_stem(f"{file.stem}-results")


def save_results(file: Path, event: Event, people: People) -> None:
    from dataclasses import asdict

    from yaml import safe_dump

    data = {
        "event": asdict(event),
        "people": {idx: asdict(person) for idx, person in enumerate(people, start=1)},
    }
    with file.open(mode="w", encoding="utf-8") as fh:
        return safe_dump(
            data, fh, allow_unicode=True, encoding="utf-8", sort_keys=False
        )
