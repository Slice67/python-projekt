from database import Database
from logger_config import setup_logger
from models.room import Room
from repositories.room_repository import RoomRepository
from services.room_service import RoomService


setup_logger()

db = Database("data/test_observatory.db")
db.initialize()

room_repository = RoomRepository(db)
room_service = RoomService(room_repository)

room = Room(
    name="Hlavní sál",
    capacity=60,
    description="Sál pro projekce a přednášky."
)

room_id = room_service.create_room(room)
print("Vytvořena místnost:", room_id)

loaded_room = room_service.get_room_by_id(room_id)
print("Načtena místnost:", loaded_room)

rooms = room_service.list_rooms()
print("Seznam místností:")
for room in rooms:
    print(room.id, room.name, room.capacity)

try:
    bad_room = Room(name="", capacity=50)
    room_service.create_room(bad_room)
except ValueError as error:
    print("Validace názvu funguje:", error)

try:
    bad_room = Room(name="Malý sál", capacity=0)
    room_service.create_room(bad_room)
except ValueError as error:
    print("Validace kapacity funguje:", error)

room_service.delete_room(room_id)
print("Místnost smazána.")

try:
    room_service.get_room_by_id(room_id)
except ValueError as error:
    print("Kontrola po smazání funguje:", error)