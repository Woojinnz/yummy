from app.database.dto.item import Item
from app.database.dto.user import User
from app.utils.database import insert_single_sql, select_sql
from typing import Sequence
from app.utils.string_func import normalize_str

def insert_one_item(i: Item, user_id: int) -> int | None:
    """  
        INSERT one menu item into the item table, 
        doesnt necessarily need to be linked to a store,

        This is a GLOBAL item
    """

    normalized_str = normalize_str(i.name)

    sql = """ INSERT INTO item (name, normalized_name, created_by) VALUES (%s,%s, %s) RETURNING id"""
    values = (i.name, normalized_str, user_id,)

    return insert_single_sql(sql,values)

def get_all_items_name_match(name: str) -> Sequence[Item]:

    """
        READ ALL items in the item table where the name is a substring match
    """

    sql = """ """

    output = []

    return output
    

if __name__ == "__main__":
    item = Item(None, "Roasted Goose")
    user = User(1, "Woojin", "wj", 0, "1234", "")

    id = insert_one_item(item, None)
    if id:
        print(id)
