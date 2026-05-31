import logging

from models.events import Event
from repositories.event_repository import EventRepository
from services import client_service, program_service, room_service, staff_service

logger = logging.getLogger(__name__)

class EventService:
    """Service pro plánované akce planetária."""

    ALLOWED_EVENT_TYPES = {
        "school_visit",
        "public_observation",
        "lecture",
        "private_booking",
        "maintenance",
        "custom",
    }

    ALLOWED_STATUSES = {
        "planned",
        "confirmed",
        "completed",
        "canceled",
    }

    def __init__(
            self, 
            event_repository: EventRepository,
            client_service,
            room_service,
            staff_service,
            program_service
    ):
        self.event_repository = event_repository
        self.client_service = client_service
        self.room_service = room_service
        self.staff_service = staff_service
        self.program_service = program_service
        
    def validate_event_basic(self, event: Event) -> None:
        """Ověří základní platnost eventu"""

        if not event.title.strip():
            raise ValueError("Název akce nesmí být prázdný")
        
        if event.event_type not in self.ALLOWED_EVENT_TYPES:
            raise ValueError(f"Neplatný typ akce: {event.event_type}")
        
        if event.status not in self.ALLOWED_STATUSES:
            raise ValueError(f"Neplatný status akce: {event.status}")
        
        if event.end_time <= event.start_time:
            raise ValueError("Konec akce musí být později než začátek")
        
        if event.visitor_count < 0:
            raise ValueError("Počet návštěvníků musí být nezáporný")
        
    def validate_event_relations(self, event: Event) -> None:
        """Ověří, že navázané entity existují"""
        
        self.client_service.get_client_by_id(event.client_id)
        self.room_service.get_room_by_id(event.room_id)
        self.staff_service.get_staff_by_id(event.staff_id)
        self.program_service.get_program_by_id(event.program_id)

    def validate_event_capacity(self, event: Event) -> None:
        """Ověří, že kapacita místnosti není překročena"""

        room = self.room_service.get_room_by_id(event.room_id)

        if event.visitor_count > room.capacity:
            raise ValueError(f"Kapacita místnosti {room.name} je {room.capacity}, ale akce má {event.visitor_count} návštěvníků.")
        
    def validate_event_conflicts(self, event: Event) -> None:
        """Ověří časové kolize místností a zaměstnance"""
        
        if self.event_repository.has_room_conflict(
            event.room_id,
            event.start_time,
            event.end_time
        ):
            raise ValueError(f"Místnost {event.room_id} je v tomto čase už obsazená")
        
        if self.event_repository.has_staff_conflict(
            event.staff_id,
            event.start_time,
            event.end_time
        ):
            raise ValueError(f"Zaměstnanec {event.staff_id} je v tomto čase už obsazený")

    def create_event(self, event: Event) -> int:
        """Zvaliduje event a uloží ho přes repository"""

        self.validate_event_basic(event)
        self.validate_event_relations(event)
        self.validate_event_capacity(event)
        self.validate_event_conflicts(event)

        event_id = self.event_repository.create_event(event)

        logger.info("Akce vytvořena | id=%d title=%s", event_id, event.title)

        return event_id
    
    def list_events(self) -> list[Event]:
        """Vrátí seznam všech akcí"""
        
        return self.event_repository.list_events()
    
    def get_event_by_id(self, event_id: int) -> Event:
        """Vrátí event podle ID nebo vyhodí výjimku"""

        event = self.event_repository.get_event_by_id(event_id)

        if event is None:
            raise ValueError(f"Akce s id {event_id} neexistuje.")
        
        return event
    
    def delete_event(self, event_id: int) -> None:
        """Smaže akci podle ID, pokud existuje"""

        self.get_event_by_id(event_id)
        
        self.event_repository.delete_event(event_id)

        logger.info("Akce s id=%d byla smazána.", event_id)