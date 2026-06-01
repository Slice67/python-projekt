from database import Database
from datetime import datetime, timedelta

from logger_config import setup_logger

from repositories.client_repository import ClientRepository
from repositories.event_repository import EventRepository
from repositories.program_repository import ProgramRepository
from repositories.room_repository import RoomRepository
from repositories.staff_repository import StaffRepository

from services.client_service import ClientService
from services.event_service import EventService
from services.export_service import ExportService
from services.program_service import ProgramService
from services.room_service import RoomService
from services.staff_service import StaffService

from ui.main_window import MainWindow

from models.clients import Client
from models.events import Event
from models.programs import Program
from models.room import Room
from models.staff import Staff


def seed_demo_data(
    client_service: ClientService,
    room_service: RoomService,
    staff_service: StaffService,
    program_service: ProgramService,
    event_service: EventService,
) -> None:
    """Vytvoří minimálně 5 záznamů pro všechny hlavní modely."""

    client_templates = [
        Client(name="ZS Komenskeho", client_type="school", contact_person="Jan Novak", email="novak@example.cz", city="Brno"),
        Client(name="Gymnazium Nova", client_type="school", contact_person="Lucie Kralova", email="kralova@example.cz", city="Praha"),
        Client(name="AstralTech s.r.o.", client_type="company", contact_person="Pavel Kratky", email="kratky@example.cz", city="Ostrava"),
        Client(name="Verejnost mesto Brno", client_type="public", contact_person="Infocentrum", email="info.brno@example.cz", city="Brno"),
        Client(name="Soukroma skupina Orion", client_type="private", contact_person="Katerina Vesela", email="vesela@example.cz", city="Plzen"),
    ]

    room_templates = [
        Room(name="Hlavni sal", capacity=120, description="Velky sal pro projekce."),
        Room(name="Maly sal", capacity=40, description="Komorne prednasky."),
        Room(name="Observator", capacity=25, description="Pozorovani oblohy."),
        Room(name="Workshop lab", capacity=30, description="Prakticke workshopy."),
        Room(name="Ucebna A", capacity=35, description="Skolni programy."),
    ]

    staff_templates = [
        Staff(name="Petr Dvorak", role="lektor", email="dvorak@example.cz"),
        Staff(name="Alena Svobodova", role="astronom", email="svobodova@example.cz"),
        Staff(name="Martin Horak", role="technik", email="horak@example.cz"),
        Staff(name="Eva Janska", role="moderator", email="janska@example.cz"),
        Staff(name="Tomas Chmel", role="koordinator", email="chmel@example.cz"),
    ]

    program_templates = [
        Program(name="Slunecni soustava", program_type="lecture", duration_minutes=90, recommended_age="10+", description="Uvod do planet."),
        Program(name="Nocni obloha", program_type="observation", duration_minutes=60, recommended_age="12+", description="Pozorovani hvezd."),
        Program(name="Meteority a komety", program_type="workshop", duration_minutes=75, recommended_age="11+", description="Interaktivni workshop."),
        Program(name="Cesta Galaxii", program_type="projection", duration_minutes=50, recommended_age="8+", description="Fulldome projekce."),
        Program(name="Astro special", program_type="custom", duration_minutes=80, recommended_age="13+", description="Tematicky special."),
    ]

    clients = client_service.list_clients()
    for index in range(len(clients), 5):
        client_service.create_client(client_templates[index])

    rooms = room_service.list_rooms()
    for index in range(len(rooms), 5):
        room_service.create_room(room_templates[index])

    staff_members = staff_service.list_staff()
    for index in range(len(staff_members), 5):
        staff_service.create_staff(staff_templates[index])

    programs = program_service.list_programs()
    for index in range(len(programs), 5):
        program_service.create_program(program_templates[index])

    clients = client_service.list_clients()
    rooms = room_service.list_rooms()
    staff_members = staff_service.list_staff()
    programs = program_service.list_programs()
    events = event_service.list_events()

    base_start = datetime(2030, 1, 1, 9, 0)
    event_types = sorted(event_service.ALLOWED_EVENT_TYPES)

    for index in range(len(events), 5):
        start_time = base_start + timedelta(days=index)
        end_time = start_time + timedelta(minutes=90)
        room = rooms[index % len(rooms)]

        event = Event(
            title=f"Demo akce {index + 1}",
            event_type=event_types[index % len(event_types)],
            start_time=start_time,
            end_time=end_time,
            visitor_count=min(20 + index * 5, room.capacity),
            client_id=clients[index % len(clients)].id,
            room_id=room.id,
            staff_id=staff_members[index % len(staff_members)].id,
            program_id=programs[index % len(programs)].id,
            status="planned",
            description="Seed data pro demonstraci aplikace.",
        )
        event_service.create_event(event)

def main() -> None:
    setup_logger()

    database = Database()
    database.initialize()

    client_service = ClientService(ClientRepository(database))
    room_service = RoomService(RoomRepository(database))
    staff_service = StaffService(StaffRepository(database))
    program_service = ProgramService(ProgramRepository(database))

    event_service = EventService(
        EventRepository(database),
        client_service,
        room_service,
        staff_service,
        program_service,
    )
    export_service = ExportService()

    seed_demo_data(client_service,room_service,staff_service,program_service,event_service,)
    
    app = MainWindow(
        client_service,
        room_service,
        staff_service,
        program_service,
        event_service,
        export_service,
    )
    app.mainloop()


if __name__ == "__main__":
    main()