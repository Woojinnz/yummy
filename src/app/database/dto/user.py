from dataclasses import dataclass

@dataclass
class User:
    id: int | None
    name: str
    username: str
    default_country: int
    password: str # probably use hashed values
    email: str