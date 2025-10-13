from dataclasses import dataclass
from typing import Optional

@dataclass
class Item:
    id: int | None
    name: str

@dataclass
class ItemImage:
    id: int | None
    store_item_id: int
    url: str
    is_primary: bool
    position: int

@dataclass
class ItemReview:
    id: int | None
    description: str
    stars: int