from dataclasses import dataclass

@dataclass
class User:
    id: int
    google_sub: str
    email: str
    name: str
    picture: str | None