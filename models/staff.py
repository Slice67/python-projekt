from dataclasses import dataclass


@dataclass
class Staff:
    name: str
    role: str
    email: str | None = None
    id: int | None = None
