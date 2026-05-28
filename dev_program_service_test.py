from database import Database
from logger_config import setup_logger
from models.programs import Program
from repositories.program_repository import ProgramRepository
from services.program_service import ProgramService


setup_logger()

db = Database("data/dev_program_service_test.db")
db.initialize()

program_repository = ProgramRepository(db)
program_service = ProgramService(program_repository)

program = Program(
    name="Sluneční soustava",
    program_type="lecture",
    duration_minutes=90,
    recommended_age="10+",
    description="Úvodní program o planetách a struktuře Sluneční soustavy."
)

program_id = program_service.create_program(program)
print("Vytvořen program:", program_id)

programs = program_service.list_programs()
for item in programs:
    print(item.id, item.name, item.program_type, item.duration_minutes, item.recommended_age)

try:
    bad_program = Program(
        name="",
        program_type="lecture",
        duration_minutes=60
    )
    program_service.create_program(bad_program)
except ValueError as error:
    print("Validace názvu funguje:", error)

try:
    bad_program = Program(
        name="Test program",
        program_type="invalid",
        duration_minutes=60
    )
    program_service.create_program(bad_program)
except ValueError as error:
    print("Validace typu funguje:", error)

try:
    bad_program = Program(
        name="Test program",
        program_type="lecture",
        duration_minutes=0
    )
    program_service.create_program(bad_program)
except ValueError as error:
    print("Validace délky funguje:", error)

loaded_program = program_service.get_program_by_id(program_id)
print("Načten program:", loaded_program)

program_service.delete_program(program_id)
print("Program smazán.")

try:
    program_service.get_program_by_id(program_id)
except ValueError as error:
    print("Kontrola po smazání funguje:", error)