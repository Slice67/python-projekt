from dataclasses import dataclass


@dataclass
class Resource:
    id: int
    name: str
    quantity: int = 1
