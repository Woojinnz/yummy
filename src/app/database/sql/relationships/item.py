from app.database.dto.item import ItemReview, ItemImage, Item
from app.database.dto.store import Store
from app.utils.string_func import normalize_str
from app.utils.database import insert_single_sql, select_sql

def insert_one_item_review(review: ItemReview, store: Store, item: Item) -> int | None:
    """ INSERT one item_review into item_review
        Find store_id with store
        Find item_id with item
        Then find the relevant mapping on store_items to find store_items.id
    """
    normalized_store = normalize_str(store.name)
    normalized_item = normalize_str(item.name)

    sql = """
    INSERT INTO item_review (store_item_id, user_id, description, stars)
    (SELECT
    ( 
        SELECT id from store_items WHERE 
        store_id = (SELECT id from store WHERE normalized_name = %s) 
        AND 
        item_id = (SELECT id from item WHERE normalized_name = %s)
    ), %s, %s, %s)
    RETURNING id
    """

    # TODO: replace hard coded user id with auth user id
    values = (normalized_store, normalized_item, review.user_id, review.description, review.stars )

    return insert_single_sql(sql, values)

def get_all_reviews_for_item_store( item: Item, store: Store) -> list[ItemReview]:
    """
    Gets all the reviews for a specifc item from a specific store
    """
    
    normalized_store = normalize_str(store.name)
    normalized_item = normalize_str(item.name)
    
    sql = """
    SELECT r.id, r.user_id, r.description, r.stars
    FROM item_review as r
    INNER JOIN store_items as si on si.id = r.store_item_id
    INNER JOIN store as s on s.id = si.store_id
    INNER JOIN item as i on i.id = si.item_id
    WHERE 
    i.normalized_name = %s
    AND
    s.normalized_name = %s
    """

    values = (normalized_store, normalized_item, )

    return select_sql(sql, values, ItemReview)


def insert_one_item_image(image: ItemImage, store: Store, item: Item) -> int | None:
    """ INSERT one item_image into item_image
        Find store_id with store
        Find item_id with item
        Then find the relevant mapping on store_items to find store_items.id
    """
    normalized_store = normalize_str(store.name)
    normalized_item = normalize_str(item.name)

    sql = """
    INSERT INTO item_image (store_item_id, image_url, is_primary, position)
    (SELECT
    ( 
        SELECT id from store_items WHERE 
        store_id = (SELECT id from store WHERE normalized_name = %s) 
        AND 
        item_id = (SELECT id from item WHERE normalized_name = %s)
    ), %s, %s, %s)
    RETURNING id
    """

    # TODO: replace hard coded user id with auth user id
    values = (normalized_store, normalized_item, image.image_url, image.is_primary, image.position )

    return insert_single_sql(sql, values)

def get_primary_image_for_item_store(item: Item, store: Store) -> list[ItemImage]:
    """
    Gets the primary image for a specifc item from a specific store
    """
    
    normalized_store = normalize_str(store.name)
    normalized_item = normalize_str(item.name)
    
    sql = """
    SELECT ii.id, ii.image_url, ii.is_primary, ii.position
    FROM item_image as ii
    INNER JOIN store_items as si on si.id = ii.store_item_id
    INNER JOIN store as s on s.id = si.store_id
    INNER JOIN item as i on i.id = si.item_id
    WHERE 
    i.normalized_name = %s
    AND
    s.normalized_name = %s
    AND 
    ii.is_primary = True
    """

    values = (normalized_store, normalized_item, )
    return select_sql(sql, values, ItemImage)

def get_all_images_for_item_store(item: Item, store: Store) -> list[ItemImage]:
    """
    Gets all the reviews for a specifc item from a specific store
    """
    
    normalized_store = normalize_str(store.name)
    normalized_item = normalize_str(item.name)
    
    sql = """
    SELECT ii.id, ii.image_url, ii.is_primary, ii.position
    FROM item_image as ii
    INNER JOIN store_items as si on si.id = ii.store_item_id
    INNER JOIN store as s on s.id = si.store_id
    INNER JOIN item as i on i.id = si.item_id
    WHERE 
    i.normalized_name = %s
    AND
    s.normalized_name = %s
    """

    values = (normalized_store, normalized_item,)
    return select_sql(sql, values, ItemImage)

if __name__ == "__main__":
    
    review = ItemReview(None, 1, "yummy", 5)
    store = Store(None, "woojin", 1)
    item = Item(None, "Roasted Goose")

    id = insert_one_item_review(review, store, item)
    if id:
        print(id)

    reviews = get_all_reviews_for_item_store(store, item)

    for r in reviews:
        print(r)

    image = ItemImage(None, "www.google.com", True, 2)

    image_id = insert_one_item_image(image, store, item)

    if image_id:
        print(image_id)

    print(get_primary_image_for_item_store(store,item))
    print(get_all_images_for_item_store(store,item))