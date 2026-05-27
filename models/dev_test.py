from clients import Client

client = Client(
    name="Škola XYZ",
    client_type="school",
    contact_person="Jan Novák",
    email="novak@example.cz",
    phone="+420123456789",
    city="Brno",
    note="Školní návštěva planetária."
)

print(client)
print(client.name)
print(client.client_type)