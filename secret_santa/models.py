from __future__ import annotations

from dataclasses import dataclass, fields
from hashlib import sha256


@dataclass(frozen=True)
class Event:
    name: str
    description: str
    manager_name: str
    manager_email: str
    kickoff_email_title: str
    kickoff_email_body: str

    def __post_init__(self) -> None:
        """Ensure mandatory fields are set, and with proper data."""
        for field in fields(self):
            if not getattr(self, field.name):
                msg = f"Event is missing the {field.name!r}!"
                raise ValueError(msg)
        if "@" not in self.manager_email:
            msg = f"Invalid 'email': {self.manager_email!r}!"
            raise ValueError(msg)

    @property
    def hash(self) -> str:
        return sha256(f"•{self.name}•".encode()).hexdigest()

    def asdict(self) -> dict[str, str]:
        return {field.name: getattr(self, field.name) for field in fields(self)}


@dataclass()
class Person:
    name: str
    nature: str
    email: str
    wishes: list[str]
    buddy: str

    def __post_init__(self) -> None:
        """Ensure mandatory fields are set, and with proper data."""
        for attr in ("name", "nature", "email"):
            if not getattr(self, attr):
                msg = f"{self} is missing the {attr!r}!"
                raise ValueError(msg)
        if "@" not in self.email:
            msg = f"Invalid 'email': {self.email!r}!"
            raise ValueError(msg)
        if self.nature not in {"maman", "papa"}:
            msg = f"Invalid 'nature': {self.nature!r}!"
            raise ValueError(msg)

    @property
    def hash(self) -> str:
        return sha256(f"{self.name}•{self.nature}•{self.email}".encode()).hexdigest()

    def asdict(self) -> dict[str, str | list[str]]:
        return {field.name: getattr(self, field.name) for field in fields(self) if field.name != "name"}


People = dict[str, Person]
