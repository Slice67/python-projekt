from dataclasses import dataclass


@dataclass
class Room:
    name: str
    capacity: int
    description: str | None = None
    id: int | None = None
