from database import Database


db = Database("data/test_observatory.db")
db.initialize()

with db.connect() as conn:
    rows = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """).fetchall()

print("Tabulky v databázi:")
for row in rows:
    print("-", row["name"])