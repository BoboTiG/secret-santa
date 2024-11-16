from pathlib import Path

import pytest

from secret_santa.models import Person

EVENT_DATA_OPENED = """
name: "[2022] Noël au moulin !"
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
sender: Zed
email: zed@localhost
"""
PEOPLE_DATA_OPENED = """
Alice:
  nature: maman
  email: alice@localhost
  wishes: []
  buddy: null
Boby:
  nature: papa
  email: boby@localhost
  wishes: []
  buddy: null
"""

EVENT_DATA_ENDED = """
name: "[2021] Noël au moulin !"
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
sender: Zed
email: zed@localhost
"""
PEOPLE_DATA_ENDED = """Alice:
  nature: maman
  email: alice@localhost
  wishes: []
  buddy: Bob
Bob:
  nature: papa
  email: bob@localhost
  wishes: []
  buddy: Alice
"""


@pytest.fixture
def ended_event(tmp_path: Path) -> Path:
    (tmp_path / "event.yml").write_text(EVENT_DATA_ENDED)
    (tmp_path / "people.yml").write_text(PEOPLE_DATA_ENDED)
    return tmp_path


@pytest.fixture
def opened_event(tmp_path: Path) -> Path:
    (tmp_path / "event.yml").write_text(EVENT_DATA_OPENED)
    (tmp_path / "people.yml").write_text(PEOPLE_DATA_OPENED)
    return tmp_path


@pytest.fixture(scope="session")
def alice() -> Person:
    return Person("Alice", "maman", "alice@localhost", [], None)


@pytest.fixture(scope="session")
def bob() -> Person:
    return Person("Bob", "papa", "bob@localhost", [], None)
