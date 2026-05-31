from database import Database
from logger_config import setup_logger

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
from services.export_service import ExportService


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

export_service = ExportService()

events = event_service.list_events()

file_path = export_service.export_events_to_csv(events)

print(f"Export hotový: {file_path}")
print(f"Počet exportovaných akcí: {len(events)}")