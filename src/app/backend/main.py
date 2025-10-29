from pathlib import Path
from dotenv import load_dotenv
import os

from fastapi.responses import FileResponse
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.sessions import SessionMiddleware

from app.utils.auth import verify_session_jwt

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

index_path = Path(__file__).resolve().parent.parent / "webapp/index.html"

from app.backend.auth.google import router as google_router

app = FastAPI()
app.include_router(google_router)
app.add_middleware(
    SessionMiddleware, 
    session_cookie = "st_session",
    secret_key=os.getenv("SESSION_SECRET"),
    same_site="lax")

@app.get("/")
def index():
    return FileResponse(index_path)

@app.get("/me")
def me(request: Request):

    token = request.cookies.get("session_jwt")
    if not token:
        raise HTTPException(401, "Not authenticated")
    
    try:
        payload = verify_session_jwt(token)
        user_id = int(payload["sub"])
    except (KeyError, ValueError):
        raise HTTPException(401, "Invalid session")

    return {"id": user_id}  