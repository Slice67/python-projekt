import logging

from models.programs import Program
from repositories.program_repository import ProgramRepository

logger = logging.getLogger(__name__)


class ProgramService:
    """Service pro programy planetária, řeší validaci a aplikační pravidla"""

    ALLOWED_PROGRAM_TYPES = {"lecture", "observation", "workshop", "projection", "custom"}

    def __init__(self, program_repository: ProgramRepository):
        self.program_repository = program_repository

    def validate_program(self, program: Program) -> None:
        """Ověří, že program má platná data"""

        if not program.name.strip():
            raise ValueError("Název programu nesmí být prázdný.")
        if program.program_type not in self.ALLOWED_PROGRAM_TYPES:
            raise ValueError(f"Neplatný typ programu. Musí být jeden z: {', '.join(sorted(self.ALLOWED_PROGRAM_TYPES))}")
        if program.duration_minutes <= 0:
            raise ValueError("Délka programu musí být kladné číslo.")

    def create_program(self, program: Program) -> int:
        """Zvaliduje program a uloží ho přes repository"""

        self.validate_program(program)
        program_id = self.program_repository.create_program(program)
        logger.info("Program vytvořen | id=%d name=%s", program_id, program.name)
        return program_id

    def list_programs(self) -> list[Program]:
        """Vrátí seznam všech programů"""
        return self.program_repository.list_programs()

    def get_program_by_id(self, program_id: int) -> Program:
        """Vrátí program podle ID nebo vyhodí výjimku, pokud neexistuje"""
        program = self.program_repository.get_program_by_id(program_id)
        if program is None:
            raise ValueError(f"Program s id={program_id} neexistuje.")
        return program

    def delete_program(self, program_id: int) -> None:
        """Smaže program podle ID, pokud existuje"""
        self.get_program_by_id(program_id)
        self.program_repository.delete_program(program_id)

        logger.info(f"Program s id={program_id} byl smazán.")