import os

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from authlib.integrations.base_client.errors import OAuthError

from app.utils.auth import issue_session_jwt, upsert_user_google
from app.backend.models.user import User


router = APIRouter(prefix="/auth/google", tags=["auth"])

config = Config(environ=os.environ)
oauth = OAuth(config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/login")
async def login_google(request: Request):
    print("Redirect URI being sent to Google:", request.url_for("callback_google"))
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri=str(request.url_for("callback_google"))
    )
    
@router.get("/callback", name="callback_google")
async def callback_google(request: Request):
    try:
 

        token = await oauth.google.authorize_access_token(request)

        userinfo = await oauth.google.parse_id_token(request, token)

        # see if email is verified, I guess reduces spam
        if not userinfo or not userinfo.get("email_verified"):
            raise HTTPException(400, "Google email is not verified")
        

        user: User = upsert_user_google(
            userinfo={
                "sub": userinfo["sub"],
                "email": userinfo["email"],
                "name": userinfo.get("name"),
                "picture": userinfo.get("picture")
            }
        )

        session_token = issue_session_jwt(user.id)
        resp = RedirectResponse(url="/")

        resp.set_cookie(
            key="session_jwt",
            value=session_token,
            httponly=True,
            samesite="lax",
            path="/",
            max_age=int(os.getenv("APP_JWT_LIFETIME_SECONDS", "43200"))
        )
        return resp
    
    except Exception as e:
        # e.error often is 'invalid_request' or 'redirect_uri_mismatch'
        # e.description tells you exactly what's wrong
        print("OAuthError:", e.error, e.description)
        raise HTTPException(400, f"OAuth error: {e.error}: {e.description}")

@router.post('/logout')
def logout():
    resp = RedirectResponse(url="/")
    resp.delete_cookie("session_jwt", path="/")
    return resp