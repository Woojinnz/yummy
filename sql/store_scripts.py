import psycopg
from dto.store import Store
from utils.string_func import normalize_str
from utils.config import load_config

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


if __name__ == "__main__":
    store = Store( None , "woojins store", 1)
    print(insert_single_store(store))