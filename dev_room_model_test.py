from models.room import Room

room = Room(
    name="Hlavní sál",
    capacity=60,
    description="Sál pro přednášky a projekce"
)

print(room)
print(room.name)
print(room.capacity)