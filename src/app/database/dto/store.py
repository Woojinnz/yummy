from dataclasses import dataclass

@dataclass
class Store:
    id: int | None
    name: str
    country_id: int

@dataclass
class Cuisine:
    id: int | None
    name: str