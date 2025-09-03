from sqlalchemy import text
from ..core.db import get_db

def test_postgres_connection():
    db = next(get_db())
    result = db.execute(text("SELECT 1")).scalar()
    assert result == 1
    
def test_tables_exist():
    db = next(get_db())
    tables = ["users", "tasks"]  # Cambia por los nombres reales de tus tablas
    for table in tables:
        result = db.execute(
            text("SELECT to_regclass(:table_name)"),
            {"table_name": table}
        ).scalar()
        assert result == table, f"La tabla '{table}' no existe en la base de datos"