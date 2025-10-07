import psycopg
from app.utils.config import load_config
from typing import Sequence, Any, LiteralString
from psycopg.rows import class_row

def insert_single_sql(sql: LiteralString, values: Sequence[Any]) -> int | None:

    id = None
    config = load_config()

    try:
        with psycopg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, values)
                rows = cur.fetchone()

                if rows:
                    id = rows[0]

                conn.commit()

    except (Exception, psycopg.DatabaseError) as error:
        print(error)
    finally:
        return id
    
def select_sql[T](sql: LiteralString, values: Sequence[Any], cls: type[T]) -> list[T]:

    rows: list[T] = []
    config = load_config()

    try:
        with psycopg.connect(**config) as conn:
            with conn.cursor(row_factory=class_row(cls)) as cur:
                cur.execute(sql, values)
                rows = cur.fetchall()

    except (psycopg.DatabaseError) as error:
        print(error)
    return rows
