# Secret Santa

![Pepe Santa](pepe-santa.png)

Secret Santa is a simple software used to distribute givers/receivers with optional wish list.

Its first use case is for Santa (Noël, in France), obviously, and it can also be used at other occasions. Be creative!

## Setup

Requires Python 3.9 (to be compatible with ZEUS).

```bash
$ python -m venv venv
$ . venv/bin/activate
$ python -m pip install -U pip wheel
$ python -m pip install -r requirements.txt
# optional: check for updates
# python -m pip list --outdated
```

## Hack

```bash
$ python -m pip install -r requirements-tests.txt
$ ./checks.sh
```

## Tests

```bash
$ python -m pip install -r requirements-tests.txt
$ python -m pytest
```

## Run

### Advert People

Send an email to all buddies with a link to the website so that they can add/update their wishes list, if any:

```bash
$ python -m secret_santa init --event FOLDER
```

### Wait for People

Start the server, it should be kept running until December, 1<sup>st</sup>:

```bash
$ python -m secret_santa front >> logs.log 2<&1
```

### Pick Santas, and Send Notifications

Optionally, setup those environment variables:

- `SS_SMTP_HOSTNAME`, ex: `mail.gandi.net`
- `SS_SMTP_USERNAME`: email ID
- `SS_SMTP_PASSWORD`: email ID password

If one of them is not set at runtime, it will be asked before sending emails.

Then it is a simple as:

```bash
$ python -m secret_santa results --event FOLDER
```

Note that you can use the command again to display results only, emails will not be sent again.
