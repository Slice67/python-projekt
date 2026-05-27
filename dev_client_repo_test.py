from database import Database
from models.clients import Client
from client_repository import ClientRepository


db = Database()
db.initialize()

client_repository = ClientRepository(db)

client1 = Client(
    name="Škola XYZ",
    client_type="school",
    contact_person="Jan Novák",
    email="novak@example.cz",
    phone="+420123456789",
    city="Brno",
    note="Školní návštěva planetária."
)


client2 = Client(
    name="Škola X",
    client_type="school",
    contact_person="Pavel Hodný",
    email="hodny@example.cz",
    phone="+420123456789",
    city="Praha",
    note="Firemní návštěva planetária."
)


client_id = client_repository.create_client(client1)
print(f"Klient 1 byl uložen s ID: {client_id}")
client_id = client_repository.create_client(client2)
print(f"Klient 2 byl uložen s ID: {client_id}")

clients = client_repository.list_clients()
print("Seznam klientů:")
for client in clients:
    print(f" - {client.name} ({client.email})")