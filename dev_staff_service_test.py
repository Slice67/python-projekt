from database import Database
from logger_config import setup_logger
from models.staff import Staff
from repositories.staff_repository import StaffRepository
from services.staff_service import StaffService


setup_logger()

db = Database("data/dev_staff_service_test.db")
db.initialize()

staff_repository = StaffRepository(db)
staff_service = StaffService(staff_repository)

staff = Staff(
    name="Petr Dvořák",
    role="technik",
    email="dvorak@example.cz"
)

staff_id = staff_service.create_staff(staff)
print("Vytvořen zaměstnanec:", staff_id)

staff_members = staff_service.list_staff()
for staff_member in staff_members:
    print(staff_member.id, staff_member.name, staff_member.role, staff_member.email)

try:
    bad_staff = Staff(name="", role="technik")
    staff_service.create_staff(bad_staff)
except ValueError as error:
    print("Validace jména funguje:", error)

try:
    bad_staff = Staff(name="Petr Dvořák", role="")
    staff_service.create_staff(bad_staff)
except ValueError as error:
    print("Validace role funguje:", error)

try:
    bad_staff = Staff(name="Petr Dvořák", role="technik", email="spatny-email")
    staff_service.create_staff(bad_staff)
except ValueError as error:
    print("Validace emailu funguje:", error)

loaded_staff = staff_service.get_staff_by_id(staff_id)
print("Načten zaměstnanec:", loaded_staff)

staff_service.delete_staff(staff_id)
print("Zaměstnanec smazán.")

try:
    staff_service.get_staff_by_id(staff_id)
except ValueError as error:
    print("Kontrola po smazání funguje:", error)