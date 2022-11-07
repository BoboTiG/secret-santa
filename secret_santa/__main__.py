from argparse import ArgumentParser
from pathlib import Path
from typing import List


def front() -> int:
    from .server import serve

    return serve()


def init(folder: Path) -> int:
    assert 0, "TODO"


def results(folder: Path) -> int:
    from .emails import send_emails
    from .picker import pick_names
    from .utils import load_data, save_results

    try:
        event, people = load_data(folder)
    except FileNotFoundError:
        print(
            f"{str(folder)!r} introuvable, prends inspiration depuis un événement passé."
        )
        print("Tu les trouveras dans le dossier 'events'.")
        return 2

    if any(person.buddy for person in people.values()):
        print()
        print("Événement :", event.name)
        print()
        print("Les résultats sont déjà connus :")
        print()
        for name, s in people.items():
            print(f"  - {s.nature.title()} Noël {name} s’occupe de {s.buddy}")
        print()
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
