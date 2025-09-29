import psycopg
from app.dto.store import Store
from app.utils.string_func import normalize_str
from app.utils.config import load_config
from typing import List

def insert_single_store(store: Store) -> int | None:
    """ INSERT a new STORE into the STORE table"""

    name_normalized: str = normalize_str(store.name)

    sql = """ INSERT INTO store (name, country_id, normalized_name) VALUES(%s, %s, %s) RETURNING id"""

    store_id = None
    config = load_config()

    try:
        with psycopg.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(sql, (store.name, store.country_id, name_normalized))
                rows = cur.fetchone()

                if rows:
                    store_id = rows[0]

                conn.commit()

    except (Exception, psycopg.DatabaseError) as error:
        print(error)
    finally:
        return store_id
    
def get_stores_using_name_country(store_name: str, country_id: int) -> List[Store]:
    """
    READ stores using LIKE name (any match since store_name) and country (exact match)
    """

    normalized_search = normalize_str(store_name)
    sql = """ SELECT * FROM store WHERE normalized_name LIKE %s AND country_id = %s """

    stores = []
    config = load_config()

    try:
        with psycopg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (f"{normalized_search}%" , country_id,))
                rows = cur.fetchall()

                for store in rows:
                    stores.append(Store(store[0], store[1], store[2]))

    except (Exception, psycopg.DatabaseError) as error:
        print(error)
    finally:
        return stores


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