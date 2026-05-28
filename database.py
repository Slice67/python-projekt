import sqlite3
from pathlib import Path

class Database:
    """Třída pro práci s databází SQLite."""
    def __init__(self, db_path: str = "data/observatory.db"): # Říká kam se uloží databáze
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)  # Vytvoří složku, pokud neexistuje
    
    def connect(self):
        connection = sqlite3.connect(self.db_path) # Otevře připojení k databázi
        connection.row_factory = sqlite3.Row  # Umožní přístup k sloupcům podle jména
        return connection
    
    def initialize(self): # Vytvoří tabulku pro klienty, pokud neexistuje
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    client_type TEXT NOT NULL,
                    contact_person TEXT,
                    email TEXT,
                    phone TEXT,
                    street TEXT,
                    city TEXT,
                    postal_code TEXT,
                    note TEXT
                    )
                """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    capacity INTEGER NOT NULL,
                    description TEXT     
                    )    
                """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS staff (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    email TEXT
                    )
                """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS programs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    program_type TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    recommended_age TEXT,
                    description TEXT
                    )
                """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    visitor_count INTEGER NOT NULL,
                    client_id INTEGER NOT NULL,
                    room_id INTEGER NOT NULL,
                    staff_id INTEGER NOT NULL,
                    program_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    description TEXT,
                    
                    FOREIGN KEY (client_id) REFERENCES clients(id),
                    FOREIGN KEY (room_id) REFERENCES rooms(id),
                    FOREIGN KEY (staff_id) REFERENCES staff(id),
                    FOREIGN KEY (program_id) REFERENCES programs(id)
                    )
                """)