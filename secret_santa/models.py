from dataclasses import dataclass, fields
from hashlib import md5
from typing import Dict, List, Union


@dataclass(frozen=True)
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

    @property
    def hash(self) -> str:
        return md5(f"•{self.name}•".encode()).hexdigest()

    def asdict(self) -> Dict[str, str]:
        return {field.name: getattr(self, field.name) for field in fields(self)}


@dataclass()
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

    @property
    def hash(self) -> str:
        return md5(f"{self.name}•{self.nature}•{self.email}".encode()).hexdigest()

    def asdict(self) -> Dict[str, Union[str, List[str]]]:
        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
            if field.name != "name"
        }


People = Dict[str, Person]
