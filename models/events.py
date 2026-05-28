from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    title: str
    event_type: str
    start_time: datetime
    end_time: datetime
    visitor_count: int
    client_id: int
    room_id: int
    staff_id: int
    program_id: int
    status: str = "planned"
    description: str | None = None
    id: int | None = None
    
