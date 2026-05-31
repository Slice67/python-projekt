import logging

from models.staff import Staff
from repositories.staff_repository import StaffRepository

logger = logging.getLogger(__name__)


class StaffService:
    """Service pro zaměstnance, řeší validaci a aplikační pravidla"""

    def __init__(self, staff_repository: StaffRepository):
        self.staff_repository = staff_repository

    def validate_staff(self, staff: Staff) -> None:
        """Ověří, že zaměstnanec má platná data"""

        if not staff.name.strip():
            raise ValueError("Jméno zaměstnance nesmí být prázdné.")
        if not staff.role.strip():
            raise ValueError("Role zaměstnance nesmí být prázdná.")
        if staff.email and "@" not in staff.email:
            raise ValueError("Neplatný formát emailu. Musí obsahovat '@'.")

    def create_staff(self, staff: Staff) -> int:
        """Zvaliduje zaměstnance a uloží ho přes repository"""

        self.validate_staff(staff)
        staff_id = self.staff_repository.create_staff(staff)
        logger.info("Zaměstnanec vytvořen | id=%d name=%s", staff_id, staff.name)
        return staff_id

    def list_staff(self) -> list[Staff]:
        """Vrátí seznam všech zaměstnanců"""
        return self.staff_repository.list_staff()

    def get_staff_by_id(self, staff_id: int) -> Staff:
        """Vrátí zaměstnance podle ID nebo vyhodí výjimku, pokud neexistuje"""
        staff = self.staff_repository.get_staff_by_id(staff_id)
        if staff is None:
            raise ValueError(f"Zaměstnanec s id={staff_id} neexistuje.")
        return staff

    def delete_staff(self, staff_id: int) -> None:
        """Smaže zaměstnance podle ID, pokud existuje"""
        self.get_staff_by_id(staff_id)
        self.staff_repository.delete_staff(staff_id)

        logger.info("Zaměstnanec s id=%d byl smazán.", staff_id)

    def update_staff(self, staff: Staff) -> None:
        """Zvaliduje zaměstnance a aktualizuje ho přes repository"""

        if staff.id is None:
            raise ValueError("ID zaměstnance je povinné.")

        self.get_staff_by_id(staff.id)
        self.validate_staff(staff)
        self.staff_repository.update_staff(staff)

        logger.info("Zaměstnanec aktualizován | id=%d name=%s", staff.id, staff.name)