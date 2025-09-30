from dataclasses import dataclass

@dataclass
class Store:
    id: int
    name: str
    country_id: int

@dataclass
class Cusisine:
    id: int
    name: str