# Secret Santa

![Pepe Santa](pepe-santa.png)

Secret Santa is a simple software used to distribute givers/receivers with optional wish list.

Its first use case is for Santa ("Noël" in France), obviously, and it can also be used at other occasions. Be creative!

## Setup

Requires Python 3.9 minimum.

```bash
python3.9 -m venv venv
. venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

### Hack

```bash
python -m pip install -r requirements-tests.txt
./checks.sh
```

### Tests

```bash
python -m pip install -r requirements-tests.txt
python -m pytest
```

## Usage

Create a folder to setup the event, lets say `2024-noel`:

```bash
mkdir noel-2024
```

Now, the tool needs two files: one with the event itself, and one with concerned people.

Create the event's event file (`noel-2024/event.yml`):

```yaml
name: "[Secret Santa 2024] Noël au moulin !"
description: |
  Salut {{ santa.nature.title() }} Noël {{ santa.name }} !

  J’ai l’honneur de te dévoiler que tu pourras faire plaisir à {{ santa.buddy }} pour Noël {{ '🎅' if santa.nature == 'papa' else '🤶' }}
  {%if buddy.wishes %}
  À titre d’information, {{ 'il' if buddy.nature == 'papa' else 'elle' }} ne serait pas contre un{{ ' (ou plusieurs)' if buddy.wishes|length > 1 else '' }} cadeau de cette liste :
  {% for wish in buddy.wishes: %}
      - {{ wish }}
  {%- endfor %}

  Bien entendu, libre à toi de suivre cette liste ou non.
  {% endif %}
  Bonne chasse aux cadeaux, et ne perd pas un rein dans l’histoire : l’important est de prendre du bon temps entre nous ❤

  La bise 💋
sender: Alice
email: alice@example.org
```

Finally, create the event's people file (`noel-2024/people.yml`):

```yaml
Alice:
  nature: maman
  email: alice@example.org
  wishes:
  - 
  buddy: null
Bob:
  nature: papa
  email: bob@example.org
  wishes:
  - 
  buddy: null
```

Add as many entries as people doing the event. Adapt the *nature* depending on the person ("papa" for a man, or "maman" for a woman).

You are good to start the event!

### First, Advert People

Send an email to all buddies with a link to the website so that they can add/update their wishes list, if any:

```bash
# In our example, replace FOLDER with 2024-noel
python -m secret_santa init --event FOLDER
```

### Second, Wait for People

Start the server, it should be kept running until December, 1<sup>st</sup>:

```bash
python -m secret_santa front >> logs.log 2<&1
```

### Finally, Pick Santa, and Send Notifications

Optionally, setup those environment variables:

- `SS_SMTP_HOSTNAME`, email server name, ex: `mail.example.org`
- `SS_SMTP_USERNAME`: email ID, ex: `alice@example.org`
- `SS_SMTP_PASSWORD`: email ID password

If one of them is not set at runtime, it will be asked before sending emails.

Then:

```bash
# In our example, replace FOLDER with 2024-noel
python -m secret_santa results --event FOLDER
```

Note that you can use the command again to only display results, emails will not be sent again.
