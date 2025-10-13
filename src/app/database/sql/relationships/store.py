from app.database.dto.store import Cuisine, Store
from app.database.dto.item import Item
from app.utils.database import insert_single_sql, select_sql
from app.utils.string_func import normalize_str
from typing import List

def add_cuisine_to_store(s: Store, c: Cuisine) -> int | None:
    """ INSERT one row mapping of store and cuisine to the STORE_CUISINES table"""

    normalized_store = normalize_str(s.name)
    normalized_cuisine = normalize_str(c.name)

    sql = """ 
    INSERT INTO store_cuisines ( store_id, cuisine_id)
    SELECT
    (SELECT id from store where normalized_name = %s),
    (SELECT id FROM cuisine WHERE normalized_name = %s)
    RETURNING id
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
    return select_sql(sql,values, Store)

def add_item_to_store(s: Store, i:Item, p: float) -> int | None:
    """ INSERT one row mapping of store and item to the store_items table"""

    normalized_store = normalize_str(s.name)
    normalized_item = normalize_str(i.name)

    sql = """ 
    
    INSERT INTO store_items (store_id, item_id, price)
    SELECT
    (SELECT id FROM store WHERE normalized_name = %s),
    (SELECT id FROM item  WHERE normalized_name = %s),
    %s
    RETURNING id;
    """
    values = (normalized_store, normalized_item, p,)
    return insert_single_sql(sql, values)

if __name__ == "__main__":

    store = Store(None, "woojin", 1)
    cuisine = Cuisine(None, "chinese")
    item = Item(None, "Roasted Goose")

    add_cusisine_id = add_cuisine_to_store(store, cuisine)
    add_item_id = add_item_to_store(store, item, 10.00)

    if add_cusisine_id:
        print(add_cusisine_id)

    if add_item_id:
        print(add_item_id)

    print(get_stores_for_cuisine(cuisine))