from dataclasses import dataclass


@dataclass
class Staff:
    id: int
    name: str
    role: str = ""
