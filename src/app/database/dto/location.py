from dataclasses import dataclass

@dataclass
class Country:
    id: int | None
    name: str
    iso_code: str
