import pytest

from secret_santa.models import Person


@pytest.fixture(scope="session")
def alice():
    return Person(
        name="Alice",
        nature="maman",
        email="alice@local.host",
        wishes=["livre"],
        buddy="",
    )


@pytest.fixture(scope="session")
def bob():
    return Person(
        name="Bob", nature="papa", email="bob@local.host", wishes=["jeans"], buddy=""
    )


@pytest.fixture
def data(alice, bob, tmp_path):
    file = tmp_path / "data.yml"
    file.write_text(
        f"""event:
  name: "[Secret Santa 2022] Noël au moulin !"
  description: |
    Salut {{{{ santa.nature.title() }}}} Noël {{{{ santa.name }}}} !

    J’ai l’honneur de te dévoiler que tu pourras faire plaisir à {{{{ santa.buddy }}}} pour Noël {{{{ '🎅' if santa.nature == 'papa' else '🤶' }}}}
    {{%if buddy.wishes %}}
    À titre d’information, {{{{ 'il' if buddy.nature == 'papa' else 'elle' }}}} ne serait pas contre un{{{{ ' (ou plusieurs)' if buddy.wishes|length > 1 else '' }}}} cadeau de cette liste :
    {{% for wish in buddy.wishes: %}}
        - {{{{ wish }}}}
    {{%- endfor %}}

    Bien entendu, libre à toi de suivre cette liste ou non.
    {{% endif %}}
    Bonne chasse aux cadeaux, et ne perd pas un rein dans l’histoire : l’important est de prendre du bon temps entre nous ❤

    La bise 💋
  sender: Zed
  email: zed@local.host

people:
  1:
    nature: {alice.nature}
    name: {alice.name}
    email: {alice.email}
    wishes: {alice.wishes}
    buddy:
  2:
    nature: {bob.nature}
    name: {bob.name}
    email: {bob.email}
    wishes: {bob.wishes}
    buddy:
"""  # noqa
    )
    return file
