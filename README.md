# Secret Santa

Secret Santa is a simple software used to distribute givers/receivers with optional wishes list.

Its first use case is for Santa (Noël, in France), obviously, and it can also be used at other occasions. Be creative!

## Setup

```bash
$ python3.11 -m venv venv
$ . venv/bin/activate
$ python -m pip install -U pip wheel
$ python -m pip install -r requirements-tests.txt
# optional: check for updates
# python -m pip list --outdated
```

## Hack

```bash
$ ./checks.sh
```

## Tests

```bash
$ python -m pytest
```

## Run

Optionally, setup those environment variables:

- `SS_SMTP_HOSTNAME`, ex: `mail.gandi.net`
- `SS_SMTP_USERNAME`: email ID
- `SS_SMTP_PASSWORD`: email ID password

If one of them is not set at runtime, it will be asked before sending emails.

Then:

```bash
$ python -m secret_santa
```
