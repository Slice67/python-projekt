from models.staff import Staff


class StaffRepository:
    def __init__(self, database):
        self.database = database

    #-------------------------------------------CREATE---------------------------------------------------------
    def create_staff(self, staff: Staff) -> int:
        with self.database.connect() as conn:
            cursor = conn.execute("""
                INSERT INTO staff(
                    name,
                    role,
                    email)
                    VALUES (?, ?, ?)
                    """, (
                        staff.name,
                        staff.role,
                        staff.email
                    ))
            return cursor.lastrowid

    # -------------------------------------------SELECT ALL---------------------------------------------------------
    def list_staff(self) -> list[Staff]:
        with self.database.connect() as conn:
            rows = conn.execute("""
                SELECT id, name, role, email
                FROM staff
                ORDER BY name
            """).fetchall()
        staff_members = []

        for row in rows:
            staff = Staff(
                id=row["id"],
                name=row["name"],
                role=row["role"],
                email=row["email"]
            )
            staff_members.append(staff)
        return staff_members

    # -------------------------------------------DELETE---------------------------------------------------------
    def delete_staff(self, staff_id: int) -> None:
        with self.database.connect() as conn:
            conn.execute("""
                DELETE FROM staff
                WHERE id = ?
            """, (staff_id,))

    # -------------------------------------------GET BY ID---------------------------------------------------------
    def get_staff_by_id(self, staff_id: int) -> Staff | None:
        with self.database.connect() as conn:
            row = conn.execute("""
                SELECT id, name, role, email
                FROM staff
                WHERE id = ?
                """,
                (staff_id,)).fetchone()
        if row is None:
            return None
        return Staff(
            id=row["id"],
            name=row["name"],
            role=row["role"],
            email=row["email"]
        )