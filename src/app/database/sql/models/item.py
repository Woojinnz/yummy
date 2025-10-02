from app.database.dto.item import Item
from app.utils.database import insert_single_sql, select_sql
from typing import Sequence

def insert_one_item(i: Item) -> int | None:
    """  
        INSERT one menu item into the item table, 
        doesnt necessarily need to be linked to a menu  
    """

    # check if (name, price,) tuple exists
    # if so that means we just need to add a new description field for this entry
    
    # the tuple matching means that there already exists an entry for this name and price.

    # does this makes sense?
    # that is how i am going to check for items that are the same

    # i guess similar shops can sell the exact same thing?
    
    # one edge case
    # store A sells (ice cream, 50)
    # store B sells (ice cream, 50)
    # obviously store A and store B will have different reviews.
    

    sql = """ INSERT INTO item (name, price) VALUES (%s,%s) RETURNING id"""
    values = (i.name, i.price)

    # need to create a new row entry in item_description to add description for the item

    return insert_single_sql(sql,values)

def get_all_items_name_match(name: str) -> Sequence[Item]:

    """
        READ ALL items in the item table where the name is a substring match
    """

    sql = """ """

    output = []

    return output
    

if __name__ == "__main__":
    item = Item(None, "Roasted Goose", 50.01, "Some roasted goose")

    id = insert_one_item(item)
    if id:
        print(id)
