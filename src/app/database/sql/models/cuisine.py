from app.database.dto.store import Cuisine
from app.database.utils.string_func import normalize_str
from app.database.utils.database import insert_single_sql, select_sql
from typing import List

def insert_one_cuisine(c: Cuisine) -> int | None:
    """ INSERT one cuisine into the CUISINE table"""

    normalized_name = normalize_str(c.name)
    
    sql = """ INSERT INTO cuisine(name, normalized_name) VALUES (%s, %s) RETURNING ID"""
    values = (c.name, normalized_name)

    return insert_single_sql(sql, values)

def get_cuisines_using_name(name: str) -> List[Cuisine]:
    """ 
    READ all cuisine with %LIKE% name (matching the start)
    c = [ Chinese, Cantonese]
    """

    sql = """SELECT id, name FROM cuisine WHERE name ILIKE %s"""
    values = (f"{name}%",)

    return select_sql(sql, values, Cuisine)

if __name__ == "__main__":
    id = insert_one_cuisine( Cuisine(None, "Chinese"))
    id_1 = insert_one_cuisine( Cuisine(None, "ChinEse"))

    if id:
        print(id)

    print(get_cuisines_using_name('c'))