from app.database.dto.store import Cuisine, Store
from app.database.utils.database import insert_single_sql, select_sql
from app.database.utils.string_func import normalize_str
from typing import List

def add_cuisine_to_store(s: Store, c: Cuisine) -> int | None:
    """ INSERT one row mapping of store and cuisine to the STORE_CUISINES table"""

    normalized_store = normalize_str(s.name)
    normalized_cuisine = normalize_str(c.name)

    sql = """ 
    
    WITH s as (
        SELECT id FROM store WHERE normalized_name = %s
    ),
    c as (
        SELECT id FROM cuisine WHERE normalized_name = %s
    )
    INSERT INTO store_cuisines (store_id, cuisine_id)
    SELECT s.id, c.id FROM s,c
    RETURNING id;
    
    """
    values = (normalized_store, normalized_cuisine,)
    return insert_single_sql(sql, values)

def get_stores_for_cuisine(c: Cuisine) -> List[Store]:
    """ READ all stores that have c cuisine """

    normalized_cuisine = normalize_str(c.name)

    sql = """

    SELECT s.id, s.name, s.country_id
    FROM store as s
    INNER JOIN store_cuisines as sc ON s.id = sc.store_id
    INNER JOIN cuisine as c on sc.cuisine_id = c.id
    WHERE c.normalized_name = %s

    """
    
    values = (normalized_cuisine,)
    return(select_sql(sql,values, Store))

if __name__ == "__main__":
    store = Store(None, "woojin", 1)
    cuisine = Cuisine(None, "chinese")
    id = add_cuisine_to_store(store, cuisine)

    if id:
        print(id)

    print(get_stores_for_cuisine(cuisine))