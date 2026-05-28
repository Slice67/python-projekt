import logging
from models.clients import Client

logger = logging.getLogger(__name__)

class ClientRepository:
    """
    Repository pro práci s klienty v databázi.
    
    Neřeší validaci, pouze CRUD operace.
    """

    def __init__(self, database): # Očekává instanci třídy Database, která se postará o připojení k databázi
        self.database = database # Ukládá instanci databáze pro pozdější použití
    
    # -------------------------------------------CREATE---------------------------------------------------------
    def create_client(self, client: Client) -> int: # Vytvoří nového klienta v databázi a vrátí jeho ID
        """Uloží klienta do databáze a vrátí jeho nové ID.
        """
        with self.database.connect() as conn:
            cursor = conn.execute("""
                INSERT INTO clients (
                    name,
                    client_type,
                    contact_person,
                    email,
                    phone,
                    street,
                    city,
                    postal_code,
                    note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, ( # Tuple s hodnotami pro jednotlivé sloupce, které se vloží do databáze
                client.name,
                client.client_type,
                client.contact_person,
                client.email,
                client.phone,
                client.street,
                client.city,
                client.postal_code,
                client.note
            ))
        return cursor.lastrowid
    
    # -------------------------------------------SELECT ALL---------------------------------------------------------
    def list_clients(self) -> list[Client]: # Vrátí seznam klientů
        with self.database.connect() as conn: # Zase připojím k db
            rows = conn.execute("""
                SELECT id, name, client_type, contact_person, email, phone, street, city, postal_code, note
                FROM clients
                ORDER BY name
            """).fetchall() # Získám všechny řádky z tabulky clients
        clients = []

        for row in rows: # Namapuju každý řádek na instanci třídy Client
            client = Client(
                id=row["id"],
                name=row["name"],
                client_type=row["client_type"],
                contact_person=row["contact_person"],
                email=row["email"],
                phone=row["phone"],
                street=row["street"],
                city=row["city"],
                postal_code=row["postal_code"],
                note=row["note"]
            )
            clients.append(client)
        return clients
    
    # -------------------------------------------DELETE---------------------------------------------------------
    def delete_client(self, client_id: int) -> None: # Smaže klienta podle ID
        """Smaže klienta z db podle jeho ID"""
        with self.database.connect() as conn:
            conn.execute("""
                DELETE FROM clients 
                WHERE id = ?
                """,
                (client_id,)) # Tuple s jedním prvkem musí mít čárku

    # -------------------------------------------GET BY ID---------------------------------------------------------
    def get_client_by_id(self, client_id: int) -> Client | None: # Vrátí klienta podle ID nebo None pokud neexistuje
        with self.database.connect() as conn:
            row = conn.execute("""
                SELECT id, name, client_type, contact_person, email, phone, street, city, postal_code, note
                FROM clients
                WHERE id = ?
            """, (client_id,)).fetchone() # Získám jeden řádek podle ID
        if row is None:
            return None
        return Client(
            id=row["id"],
            name=row["name"],
            client_type=row["client_type"],
            contact_person=row["contact_person"],
            email=row["email"],
            phone=row["phone"],
            street=row["street"],
            city=row["city"],
            postal_code=row["postal_code"],
            note=row["note"]
        )