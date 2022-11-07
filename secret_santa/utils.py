from pathlib import Path
from typing import Tuple

from .models import Event, People, Person


def load_data(folder: Path) -> Tuple[Event, People]:
    from yaml import safe_load

    with (folder / "event.yml").open(encoding="utf-8") as fh:
        event = Event(**safe_load(fh))
    with (folder / "people.yml").open(encoding="utf-8") as fh:
        people = {
            name: Person(name, **details) for name, details in safe_load(fh).items()
        }
    return event, people


def save_results(folder: Path, people: People) -> None:
    from yaml import safe_dump

    data = {name: person.asdict() for name, person in people.items()}
    file = folder / "people.yml"
    with file.open(mode="w", encoding="utf-8") as fh:
        return safe_dump(
            data, fh, allow_unicode=True, encoding="utf-8", sort_keys=False
        )
