from dataclasses import dataclass
from typing import List


@dataclass(frozen=True, slots=True)
class Event:
    name: str
    description: str
    sender: str
    email: str


@dataclass(slots=True)
class Person:
    name: str
    nature: str
    email: str
    wishes: List[str]
    buddy: str


People = List[Person]
