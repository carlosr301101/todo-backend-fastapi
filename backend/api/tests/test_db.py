from sqlalchemy import text
from ..core.db import get_db

def test_postgres_connection():
    db = next(get_db())
    result = db.execute(text("SELECT 1")).scalar()
    assert result == 1