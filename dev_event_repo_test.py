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


setup_logger()

db = Database("data/test_observatory.db")
db.initialize()

client_service = ClientService(ClientRepository(db))
room_service = RoomService(RoomRepository(db))
staff_service = StaffService(StaffRepository(db))
program_service = ProgramService(ProgramRepository(db))
event_repository = EventRepository(db)

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
    description="Školní návštěva s programem o Sluneční soustavě.",
)

event_id = event_repository.create_event(event)
print("Vytvořen event:", event_id)

loaded_event = event_repository.get_event_by_id(event_id)
print("Načten event:", loaded_event)
print(type(loaded_event.start_time))
print(type(loaded_event.end_time))

events = event_repository.list_events()
print("Seznam eventů:")
for event in events:
    print(event.id, event.title, event.start_time, event.end_time)

has_room_conflict = event_repository.has_room_conflict(
    room_id=room_id,
    start_time=datetime(2026, 6, 1, 10, 30),
    end_time=datetime(2026, 6, 1, 11, 0),
)
print("Kolize místnosti:", has_room_conflict)

has_staff_conflict = event_repository.has_staff_conflict(
    staff_id=staff_id,
    start_time=datetime(2026, 6, 1, 10, 30),
    end_time=datetime(2026, 6, 1, 11, 0),
)
print("Kolize zaměstnance:", has_staff_conflict)

event_repository.delete_event(event_id)
print("Event smazán.")