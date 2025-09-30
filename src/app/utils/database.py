import psycopg
from app.utils.config import load_config
from typing import List, TypeVar, Sequence, Type
from psycopg.rows import class_row

T = TypeVar('T')

def insert_single_sql(sql: str, values: Sequence[object]) -> int | None:

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
    
def select_sql(sql: str, values: Sequence[object], cls: Type[T]) -> List[T]:

    config = load_config()

    try:
        with psycopg.connect(**config, row_factory=class_row(cls)) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, values)
                return cur.fetchall()

    except (Exception, psycopg.DatabaseError) as error:
        print(error)
        return []
