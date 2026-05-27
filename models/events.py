from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    id: int
    name: str
    starts_at: datetime
    program_id: int | None = None
    staff_ids: list[int] = field(default_factory=list)
    resource_ids: list[int] = field(default_factory=list)
