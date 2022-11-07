from dataclasses import dataclass, fields
from typing import List


@dataclass(frozen=True, slots=True)
class Event:
    name: str
    description: str
    sender: str
    email: str

    def __post_init__(self) -> None:
        """Ensure mandatory fields are set, and with proper data."""
        for field in fields(self):
            if not getattr(self, field.name):
                raise ValueError(f"Event is missing the {field.name!r}!")
        if "@" not in self.email:
            raise ValueError(f"Invalid 'email': {self.email!r}!")


@dataclass(slots=True)
class Person:
    name: str
    nature: str
    email: str
    wishes: List[str]
    buddy: str

    def __post_init__(self) -> None:
        """Ensure mandatory fields are set, and with proper data."""
        for attr in {"name", "nature", "email"}:
            if not getattr(self, attr):
                raise ValueError(f"{self} is missing the {attr!r}!")
        if "@" not in self.email:
            raise ValueError(f"Invalid 'email': {self.email!r}!")
        if self.nature not in {"maman", "papa"}:
            raise ValueError(f"Invalid 'nature': {self.nature!r}!")


People = List[Person]
