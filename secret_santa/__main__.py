from argparse import ArgumentParser
from pathlib import Path
from typing import List

from .models import Event, People


def has_ended(event: Event, people: People) -> bool:
    if any(person.buddy for person in people.values()):
        print()
        print("Événement :", event.name)
        print()
        print("Les résultats sont déjà connus :")
        print()
        for name, s in people.items():
            print(f"  - {s.nature.title()} Noël {name} s’occupe de {s.buddy}")
        print()
        return True
    return False


def front() -> int:
    from .server import serve

    return serve()


def init(folder: Path) -> int:
    from .constants import INIT_EVENT_DESC, INIT_EVENT_NAME
    from .emails import init_msg, send_emails
    from .utils import load_data

    event, people = load_data(folder)
    if has_ended(event, people):
        return 1

    name = INIT_EVENT_NAME.format(event.name)
    event_init = Event(name, INIT_EVENT_DESC, event.sender, event.email)

    send_emails(event_init, people, msg_body_fn=init_msg)
    return 0


def results(folder: Path) -> int:
    from .emails import send_emails
    from .picker import pick_names
    from .utils import load_data, save_results

    event, people = load_data(folder)
    if has_ended(event, people):
        return 1

    secret_santas = pick_names(people)
    save_results(folder, secret_santas)
    send_emails(event, secret_santas)
    return 0


def folder(name: str) -> Path:
    return Path(name or "placeholder")


def main(cli_args: List[str]) -> int:
    parser = ArgumentParser(description="Secret Santa!", allow_abbrev=False)
    parser.add_argument("action", type=str, choices=["front", "init", "results"])
    parser.add_argument("--event", type=folder)

    ret, args = 0, parser.parse_args(cli_args)
    match args.action:
        case "front":
            ret = front()
        case "init":
            ret = init(args.event)
        case "results":
            ret = results(args.event)
    return ret


if __name__ == "__main__":  # pragma: nocover
    import contextlib
    import sys

    ret = 0
    with contextlib.suppress(KeyboardInterrupt):
        ret = main(sys.argv[1:])
    sys.exit(ret)
