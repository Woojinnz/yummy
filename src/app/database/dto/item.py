from dataclasses import dataclass
from typing import Optional

@dataclass
class Item:
    id: int | None
    name: str

@dataclass
class ItemImage:
    id: int | None
    item_id: int
    url: str
    is_primary: bool
    position: int
