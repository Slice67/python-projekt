from models.room import Room

class RoomRepository:
    def __init__(self, database):
        self.database = database
    
    #-------------------------------------------CREATE---------------------------------------------------------
    def create_room(self, room: Room) -> int:
        with self.database.connect() as conn:
            cursor = conn.execute("""
                INSERT INTO rooms(
                    name,
                    capacity,
                    description)
                    VALUES (?, ?, ?)
                    """, (
                        room.name,
                        room.capacity,
                        room.description
                    ))
            return cursor.lastrowid
        
    # -------------------------------------------SELECT ALL---------------------------------------------------------
    def list_rooms(self) -> list[Room]:
        with self.database.connect() as conn:
            rows = conn.execute("""
                SELECT id, name, capacity, description
                FROM rooms
                ORDER BY name
            """).fetchall()
        rooms = []

        for row in rows:
            room = Room(
                id=row["id"],
                name=row["name"],
                capacity=row["capacity"],
                description=row["description"]
            )
            rooms.append(room)
        return rooms
    
    # -------------------------------------------DELETE---------------------------------------------------------
    def delete_room(self, room_id: int) -> None:
        """Smaže místnost z db podle jejího ID"""

        with self.database.connect() as conn:
            conn.execute("""
                DELETE FROM rooms
                WHERE id = ?
            """, (room_id,))

    # -------------------------------------------GET BY ID---------------------------------------------------------
    def get_room_by_id(self, room_id: int) -> Room | None:
        with self.database.connect() as conn:
            row = conn.execute("""
                SELECT id, name, capacity, description
                FROM rooms
                WHERE id = ?
                """,
                (room_id,)).fetchone()
        if row is None:
            return None
        return Room(
            id=row["id"],
            name=row["name"],
            capacity=row["capacity"],
            description=row["description"]
        )
    
    #-------------------------------------------UPDATE---------------------------------------------------------
    def update_room(self, room: Room) -> None:
        with self.database.connect() as conn:
            conn.execute("""
                UPDATE rooms
                SET name = ?, capacity = ?, description = ?
                WHERE id = ?
            """, (
                room.name,
                room.capacity,
                room.description,
                room.id
            ))