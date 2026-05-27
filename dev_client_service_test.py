
from database import Database
from logger_config import setup_logger
from models.clients import Client
from repositories.client_repository import ClientRepository
from services.client_service import ClientService


setup_logger()

db = Database()
db.initialize()

client_repository = ClientRepository(db)
client_service = ClientService(client_repository)

client = Client(
    name="ZŠ Komenského",
    client_type="school",
    contact_person="Jan Novák",
    email="novak@example.cz",
    city="Brno"
)

client_id = client_service.create_client(client)
print("Vytvořen klient:", client_id)

clients = client_service.list_clients()

for client in clients:
    print(client.id, client.name, client.client_type)