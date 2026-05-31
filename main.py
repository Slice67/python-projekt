from database import Database
from logger_config import setup_logger

from repositories.client_repository import ClientRepository
from repositories.event_repository import EventRepository
from repositories.program_repository import ProgramRepository
from repositories.room_repository import RoomRepository
from repositories.staff_repository import StaffRepository

from services import program_service
from services.client_service import ClientService
from services.event_service import EventService
from services.export_service import ExportService
from services.program_service import ProgramService
from services.room_service import RoomService
from services.staff_service import StaffService

from ui.main_window import MainWindow

from models.clients import Client
from models.room import Room
from models.staff import Staff
from models.programs import Program

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

    def seed_demo_data(client_service, room_service, staff_service, program_service) -> None:
        if not client_service.list_clients():
            client_service.create_client(Client(
                name="ZŠ Komenského",
                client_type="school",
                contact_person="Jan Novák",
                email="novak@example.cz",
            ))

        if not room_service.list_rooms():
            room_service.create_room(Room(
                name="Hlavní sál",
                capacity=60,
                description="Sál pro projekce a přednášky.",
            ))

        if not staff_service.list_staff():
            staff_service.create_staff(Staff(
                name="Petr Dvořák",
                role="lektor",
                email="dvorak@example.cz",
            ))

        if not program_service.list_programs():
            program_service.create_program(Program(
                name="Sluneční soustava",
                program_type="lecture",
                duration_minutes=90,
                recommended_age="10+",
                description="Úvodní program o planetách a struktuře Sluneční soustavy.",
            ))
    seed_demo_data(client_service, room_service, staff_service, program_service)
    
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