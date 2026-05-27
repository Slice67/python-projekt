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