from dataclasses import dataclass

@dataclass
class Store:
    id: int
    name: str
    country_id: int

@dataclass
class Cuisine:
    id: int
    name: str