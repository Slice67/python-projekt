from dataclasses import dataclass


@dataclass
class Program:
    name: str
    program_type: str
    duration_minutes: int
    recommended_age: str | None = None
    description: str | None = None
    id: int | None = None
