from models.programs import Program

class ProgramRepository:
    def __init__(self, database):
        self.database = database

    #-------------------------------------------CREATE---------------------------------------------------------
    def create_program(self, program: Program) -> int:
        with self.database.connect() as conn:
            cursor = conn.execute("""
                INSERT INTO programs(
                    name,
                    program_type,
                    duration_minutes,
                    recommended_age,
                    description)
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        program.name,
                        program.program_type,
                        program.duration_minutes,
                        program.recommended_age,
                        program.description,
                    ))
            return cursor.lastrowid

    # -------------------------------------------SELECT ALL---------------------------------------------------------
    def list_programs(self) -> list[Program]:
        with self.database.connect() as conn:
            rows = conn.execute("""
                SELECT id, name, program_type, duration_minutes, recommended_age, description
                FROM programs
                ORDER BY name
            """).fetchall()
        programs = []

        for row in rows:
            program = Program(
                id=row["id"],
                name=row["name"],
                program_type=row["program_type"],
                duration_minutes=row["duration_minutes"],
                recommended_age=row["recommended_age"],
                description=row["description"]
            )
            programs.append(program)
        return programs

    # -------------------------------------------DELETE---------------------------------------------------------
    def delete_program(self, program_id: int) -> None:
        with self.database.connect() as conn:
            conn.execute("""
                DELETE FROM programs
                WHERE id = ?
            """, (program_id,))

    # -------------------------------------------GET BY ID---------------------------------------------------------
    def get_program_by_id(self, program_id: int) -> Program | None:
        with self.database.connect() as conn:
            row = conn.execute("""
                SELECT id, name, program_type, duration_minutes, recommended_age, description
                FROM programs
                WHERE id = ?
                """,
                (program_id,)).fetchone()
        if row is None:
            return None
        return Program(
            id=row["id"],
            name=row["name"],
            program_type=row["program_type"],
            duration_minutes=row["duration_minutes"],
            recommended_age=row["recommended_age"],
            description=row["description"]
        )

    #-------------------------------------------UPDATE---------------------------------------------------------
    def update_program(self, program: Program) -> None:
        with self.database.connect() as conn:
            conn.execute("""
                UPDATE programs
                SET name = ?, program_type = ?, duration_minutes = ?, recommended_age = ?, description = ?
                WHERE id = ?
            """, (
                program.name,
                program.program_type,
                program.duration_minutes,
                program.recommended_age,
                program.description,
                program.id,
            ))
