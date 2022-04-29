# Secret Santa

## Setup

## Hack

```bash
$ python -m black secret_santa
$ python -m flake8 secret_santa
```

## Tests

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
