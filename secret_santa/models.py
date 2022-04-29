from dataclasses import dataclass
from typing import List


@dataclass
class Event:
    name: str
    description: str
    sender: str
    email: str


@dataclass
class Person:
    name: str
    nature: str
    email: str
    wishes: List[str]
    buddy: str


People = List[Person]
