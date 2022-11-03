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


@pytest.fixture(scope="session")
def data(tmp_path):
    file = tmp_path / "data.yml"
    file.write_text(...)
    return file
