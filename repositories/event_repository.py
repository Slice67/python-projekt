from models.events import Event
from datetime import datetime

class EventRepository:
    def __init__(self, database):
        self.database = database
    
    #-------------------------------------------CREATE---------------------------------------------------------
    def create_event(self, event: Event) -> int:
        with self.database.connect() as conn:
            cursor = conn.execute("""
                INSERT INTO events(
                    title,
                    event_type,
                    start_time,
                    end_time,
                    visitor_count,
                    client_id,
                    room_id,
                    staff_id,
                    program_id,
                    status,
                    description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        event.title,
                        event.event_type,
                        event.start_time.isoformat(),
                        event.end_time.isoformat(),
                        event.visitor_count,
                        event.client_id,
                        event.room_id,
                        event.staff_id,
                        event.program_id,
                        event.status,
                        event.description
                    ))
            return cursor.lastrowid
    
    # -------------------------------------------SELECT ALL---------------------------------------------------------
    def list_events(self) -> list[Event]:
        with self.database.connect() as conn:
            rows = conn.execute("""
                SELECT id, title, event_type, start_time, end_time, visitor_count, client_id, room_id, staff_id, program_id, status, description
                FROM events
                ORDER BY start_time
            """).fetchall()
        events = []

        for row in rows:
            event = Event(
                id=row["id"],
                title=row["title"],
                event_type=row["event_type"],
                start_time=datetime.fromisoformat(row["start_time"]),
                end_time=datetime.fromisoformat(row["end_time"]),
                visitor_count=row["visitor_count"],
                client_id=row["client_id"],
                room_id=row["room_id"],
                staff_id=row["staff_id"],
                program_id=row["program_id"],
                status=row["status"],
                description=row["description"]
            )
            events.append(event)
        return events
    
    # -------------------------------------------DELETE---------------------------------------------------------
    def delete_event(self, event_id: int) -> None:
        with self.database.connect() as conn:
            conn.execute("""
                DELETE FROM events
                WHERE id = ?
            """, (event_id,))

    # -------------------------------------------GET BY ID---------------------------------------------------------
    def get_event_by_id(self, event_id: int) -> Event | None:
        with self.database.connect() as conn:
            row = conn.execute("""
                SELECT id, title, event_type, start_time, end_time, visitor_count, client_id, room_id, staff_id, program_id, status, description
                FROM events
                WHERE id = ?
                """,
                (event_id,)).fetchone()
        if row is None:
            return None
        return Event(
            id=row["id"],
            title=row["title"],
            event_type=row["event_type"],
            start_time=datetime.fromisoformat(row["start_time"]),
            end_time=datetime.fromisoformat(row["end_time"]),
            visitor_count=row["visitor_count"],
            client_id=row["client_id"],
            room_id=row["room_id"],
            staff_id=row["staff_id"],
            program_id=row["program_id"],
            status=row["status"],
            description=row["description"]
        )
    
    # -----------------------------------KOLIZE S MÍSTNOSTÍ-----------------------------------------------------
    def has_room_conflict(self, room_id: int, start_time: datetime, end_time: datetime, ignored_event_id: int | None = None,) -> bool:
        query = """
            SELECT COUNT(*) AS count
            FROM events
            WHERE room_id = ?
                AND status != 'cancelled'
                AND start_time < ?
                AND end_time > ?
        """
        
        params = [room_id,
            end_time.isoformat(),
            start_time.isoformat()
        ]

        if ignored_event_id is not None:
            query += " AND id != ?"
            params.append(ignored_event_id) # Pokud aktualizujeme existující akci, nechceme, aby se kontrolovala kolize s ní samotnou

        with self.database.connect() as conn:
            row = conn.execute(query, params).fetchone()
            
        return row["count"] > 0
    
    # -----------------------------------KOLIZE S ZAMĚSTNANCEM-----------------------------------------------------
    def has_staff_conflict(self, staff_id: int, start_time: datetime, end_time: datetime, ignored_event_id: int | None = None) -> bool:
        query = """
            SELECT COUNT(*) AS count
            FROM events
            WHERE staff_id = ?
                AND status != 'cancelled'
                AND start_time < ?
                AND end_time > ?
        """
        
        params = [staff_id,
            end_time.isoformat(),
            start_time.isoformat()
        ]

        if ignored_event_id is not None:
            query += " AND id != ?"
            params.append(ignored_event_id)

        with self.database.connect() as conn:
            row = conn.execute(query, params).fetchone()
            
        return row["count"] > 0
    
    #-------------------------------------------UPDATE---------------------------------------------------------
    def update_event(self, event: Event) -> None:
        with self.database.connect() as conn:
            conn.execute("""
                UPDATE events
                SET 
                    title = ?, 
                    event_type = ?, 
                    start_time = ?, 
                    end_time = ?, 
                    visitor_count = ?, 
                    client_id = ?, 
                    room_id = ?, staff_id = ?, 
                    program_id = ?, 
                    status = ?, 
                    description = ?
                WHERE id = ?
            """, (
                event.title,
                event.event_type,
                event.start_time.isoformat(),
                event.end_time.isoformat(),
                event.visitor_count,
                event.client_id,
                event.room_id,
                event.staff_id,
                event.program_id,
                event.status,
                event.description,
                event.id
            ))