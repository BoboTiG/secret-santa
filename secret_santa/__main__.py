from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from secret_santa.models import Event, People


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
    from .emails import send_emails
    from .utils import create_init_emails, load_data

    event, people = load_data(folder)
    if has_ended(event, people):
        return 1

    messages = create_init_emails(event, people)
    send_emails(messages)

    return 0


def results(folder: Path) -> int:
    from .emails import send_emails, smtp_connexion
    from .picker import pick_names
    from .utils import create_results_emails, load_data, save_results

    event, people = load_data(folder)
    if has_ended(event, people):
        return 1

    # Early connexion to ensure emails can be sent
    smtp_conn = smtp_connexion()

    secret_santas = pick_names(people)
    save_results(folder, secret_santas)

    messages = create_results_emails(event, people)
    send_emails(messages, conn=smtp_conn)

    return 0


def folder(name: str) -> Path:
    return Path(name or "placeholder")


def main(cli_args: list[str]) -> int:
    parser = ArgumentParser(description="Secret Santa!", allow_abbrev=False)
    parser.add_argument("action", type=str, choices=["front", "init", "results"])
    parser.add_argument("--event", type=folder)

    ret, args = 0, parser.parse_args(cli_args)
    if args.action == "front":
        ret = front()
    elif args.action == "init":
        ret = init(args.event)
    elif args.action == "results":
        ret = results(args.event)
    return ret


if __name__ == "__main__":  # pragma: nocover
    import contextlib
    import sys

    ret = 0
    with contextlib.suppress(KeyboardInterrupt):
        ret = main(sys.argv[1:])
    sys.exit(ret)
