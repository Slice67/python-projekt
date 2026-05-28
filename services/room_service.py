import logging

from models.room import Room
from repositories.room_repository import RoomRepository

logger = logging.getLogger(__name__)

class RoomService:
    """Service pro místnosti, řeší validaci a aplikační pravidla"""

    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def validate_room(self, room: Room) -> None:
        """Ověří že místnost má platná data"""

        if not room.name.strip():
            raise ValueError("Název místnosti nesmí být prázdný.")
        if room.capacity <= 0:
            raise ValueError("Kapacita místnosti musí být kladné číslo.")
        
    def create_room(self, room: Room) -> int:
        """Zvaliduje místnost a uloží ji přes repository"""

        self.validate_room(room)
        room_id = self.room_repository.create_room(room)
        logger.info(f"Místnost vytvořena | id={room_id} name={room.name}")
        return room_id
    
    def list_rooms(self) -> list[Room]:
        """Vrátí seznam všech místností"""
        return self.room_repository.list_rooms()
    
    def get_room_by_id(self, room_id: int) -> Room:
        """Vrátí místnost podle ID nebo vyhodí výjimku, pokud neexistuje"""
        room = self.room_repository.get_room_by_id(room_id)
        if room is None:
            raise ValueError(f"Místnost s id={room_id} neexistuje.")
        return room
    
    def delete_room(self, room_id: int) -> None:
        """Smaže místnost podle ID, pokud existuje"""
        self.get_room_by_id(room_id)
        self.room_repository.delete_room(room_id)

        logger.info(f"Místnost s id={room_id} byla smazána.")