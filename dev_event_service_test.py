from datetime import datetime

from database import Database
from logger_config import setup_logger

from models.clients import Client
from models.room import Room
from models.staff import Staff
from models.programs import Program
from models.events import Event

from repositories.client_repository import ClientRepository
from repositories.room_repository import RoomRepository
from repositories.staff_repository import StaffRepository
from repositories.program_repository import ProgramRepository
from repositories.event_repository import EventRepository

from services.client_service import ClientService
from services.room_service import RoomService
from services.staff_service import StaffService
from services.program_service import ProgramService
from services.event_service import EventService


setup_logger()

db = Database("data/test_observatory.db")
db.initialize()

client_service = ClientService(ClientRepository(db))
room_service = RoomService(RoomRepository(db))
staff_service = StaffService(StaffRepository(db))
program_service = ProgramService(ProgramRepository(db))

event_service = EventService(
    EventRepository(db),
    client_service,
    room_service,
    staff_service,
    program_service,
)

client_id = client_service.create_client(Client(
    name="ZŠ Komenského",
    client_type="school",
    contact_person="Jan Novák",
    email="novak@example.cz",
))

room_id = room_service.create_room(Room(
    name="Hlavní sál",
    capacity=60,
))

staff_id = staff_service.create_staff(Staff(
    name="Petr Dvořák",
    role="lektor",
    email="dvorak@example.cz",
))

program_id = program_service.create_program(Program(
    name="Sluneční soustava",
    program_type="lecture",
    duration_minutes=90,
    recommended_age="10+",
))

event = Event(
    title="Návštěva ZŠ Komenského",
    event_type="school_visit",
    start_time=datetime(2026, 6, 1, 10, 0),
    end_time=datetime(2026, 6, 1, 11, 30),
    visitor_count=28,
    client_id=client_id,
    room_id=room_id,
    staff_id=staff_id,
    program_id=program_id,
    status="planned",
    description="Školní návštěva planetária.",
)

try:
    too_large_event = Event(
        title="Přeplněná návštěva",
        event_type="school_visit",
        start_time=datetime(2026, 6, 2, 10, 0),
        end_time=datetime(2026, 6, 2, 11, 30),
        visitor_count=100,
        client_id=client_id,
        room_id=room_id,
        staff_id=staff_id,
        program_id=program_id,
        status="planned",
    )
    event_service.create_event(too_large_event)
except ValueError as error:
    print("Validace kapacity funguje:", error)


try:
    conflicting_event = Event(
        title="Kolizní akce",
        event_type="lecture",
        start_time=datetime(2026, 6, 1, 10, 30),
        end_time=datetime(2026, 6, 1, 11, 0),
        visitor_count=20,
        client_id=client_id,
        room_id=room_id,
        staff_id=staff_id,
        program_id=program_id,
        status="planned",
    )
    event_service.create_event(conflicting_event)
except ValueError as error:
    print("Validace kolize funguje:", error)

try:
    too_large_event = Event(
        title="Přeplněná návštěva",
        event_type="school_visit",
        start_time=datetime(2026, 6, 2, 10, 0),
        end_time=datetime(2026, 6, 2, 11, 30),
        visitor_count=100,
        client_id=client_id,
        room_id=room_id,
        staff_id=staff_id,
        program_id=program_id,
        status="planned",
    )
    event_service.create_event(too_large_event)
except ValueError as error:
    print("Validace kapacity funguje:", error)

try:
    conflicting_event = Event(
        title="Kolizní akce",
        event_type="lecture",
        start_time=datetime(2026, 6, 1, 10, 30),
        end_time=datetime(2026, 6, 1, 11, 0),
        visitor_count=20,
        client_id=client_id,
        room_id=room_id,
        staff_id=staff_id,
        program_id=program_id,
        status="planned",
    )
    event_service.create_event(conflicting_event)
except ValueError as error:
    print("Validace kolize funguje:", error)

event_service.validate_event_basic(event)
print("Základní validace validního eventu prošla.")

event_service.validate_event_relations(event)
print("Validace vazeb prošla.")
