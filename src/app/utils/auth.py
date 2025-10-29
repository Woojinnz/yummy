import os
from datetime import datetime, timedelta, timezone

from jose import jwt

from app.backend.models.user import User

# DB OPERATIONS
from app.database.sql.models.user import get_user_by_google_sub, insert_user_google

ISS = os.getenv("APP_JWT_ISS", "yummy")
SECRET = os.getenv("APP_JWT_SECRET")
LIFETIME = int(os.getenv("APP_JWT_LIFETIME_SECONDS", "43200"))

def issue_session_jwt(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iss": ISS,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=LIFETIME)).timestamp()),
        "typ": "session",
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_session_jwt(token: str) -> dict:
    return jwt.decode(
        token,
        SECRET,
        algorithms=["HS256"],
        issuer=ISS,
        options={"require": ["exp", "iat"]},
    )
    

def upsert_user_google(userInfo: User):

    ui = User.model_validate(userInfo)
    user_db = get_user_by_google_sub(ui.sub)
    if user_db:
        return user_db
    
    insert_user_google(
        google_sub=ui.sub,
        email=ui.email,
        name=ui.name,
        picture=ui.picture
    )

    created = get_user_by_google_sub(ui.sub)

    if not created:
        raise RuntimeError("User added to DB but could not be found")
    

    new_user: User = User(
        sub=created.google_sub,
        email=created.email,
        name=created.name,
        picture=created.picture
    )

    return new_user
