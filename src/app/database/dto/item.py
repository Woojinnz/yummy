from dataclasses import dataclass
from typing import Optional

@dataclass
class Item:
    id: int | None
    name: str

@dataclass
class ItemImage:
    id: int | None
    image_url: str
    is_primary: bool
    position: int

@dataclass
class ItemReview:
    id: int | None
    user_id: int
    description: str
    stars: int