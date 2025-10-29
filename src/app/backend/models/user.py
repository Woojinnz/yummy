from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    sub: str
    email: str
    name:str 
    picture: str | None = None
    when: datetime