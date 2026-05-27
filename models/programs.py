from dataclasses import dataclass


@dataclass
class Program:
    id: int
    name: str
    description: str = ""
