from app.database.dto.store import Store
from app.database.utils.string_func import normalize_str
from typing import List
from app.database.utils.database import insert_single_sql, select_sql

def insert_single_store(store: Store) -> int | None:
    """ INSERT a new STORE into the STORE table"""

    name_normalized: str = normalize_str(store.name)
    sql = """ INSERT INTO store (name, country_id, normalized_name) VALUES(%s, %s, %s) RETURNING id"""

    values = (store.name, store.country_id, name_normalized)
    return insert_single_sql(sql, values)

def get_stores_using_name_country(store_name: str, country_id: int) -> List[Store]:
    """
    READ stores using LIKE name (any match since store_name) and country (exact match)
    """

    normalized_search = normalize_str(store_name)

    sql = """ SELECT id, name, country_id FROM store WHERE normalized_name LIKE %s AND country_id = %s """
    values = (f"{normalized_search}%" , country_id,)
    return select_sql(sql, values, Store)

if __name__ == "__main__":
    store = Store( None , "woojins store", 1)
    id = insert_single_store(store)
    if id:
        print(id, end="\n")

    store = Store( None , "woojin", 1)
    id = insert_single_store(store)
    if id:
        print(id, end="\n")

    print(get_stores_using_name_country("WOOJI", 1))