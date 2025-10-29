from app.database.dto.user import User
from app.utils.database import insert_single_sql, select_sql

def insert_user_google(*, google_sub: str, email: str, name: str, picture: str | None = None):
    """Insert a new user, return new id."""

    sql = """
        INSERT INTO users (google_sub, email, name, picture)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """
    values = (google_sub, email, name, picture)
    return insert_single_sql(sql, values)

def get_user_by_google_sub(google_sub: str) -> User | None:

    sql = """SELECT id, google_sub, email, name, picture FROM users WHERE google_sub = %s"""
    return select_sql(sql, (google_sub,), User)