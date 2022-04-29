from pathlib import Path
import sys


def main(data: Path) -> int:
    from .emails import send_emails
    from .picker import pick_names
    from .utils import load_data, result_file, save_results

    result = result_file(data)
    if result.is_file():
        event, people = load_data(result)
        print()
        print("Événement :", event.name)
        print()
        print("Les résultats sont déjà connus :")
        print()
        for s in people:
            print(f"  - {s.nature.title()} Noël {s.name} s’occupe de {s.buddy}")
        print()
        return 1

    if not data.is_file():
        print(
            f"{str(data)!r} introuvable, prends inspiration depuis un événement passé."
        )
        print("Tu les trouveras dans le dossier 'events'.")
        return 2

    event, people = load_data(data)
    secret_santas = pick_names(people)
    save_results(result, event, secret_santas)
    send_emails(event, secret_santas)
    return 0


def usage() -> int:
    print("python -m secret_santa FILE.yml")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(Path(sys.argv[1])))
    except (IndexError, TypeError):
        # IndexError when there is no enough arfuments
        # TypeError when the argument is not a proper YAML file
        sys.exit(usage())
