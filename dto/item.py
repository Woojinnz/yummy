from dataclasses import dataclass

@dataclass
class Item:
    id: int
    name: str
    price: float

@dataclass
class ItemImage:
    id: int
    item_id: int
    url: str
    is_primary: bool
    position: int
