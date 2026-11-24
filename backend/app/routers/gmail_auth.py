import json
import os
from pathlib import Path

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from app.core.oauth import oauth

router = APIRouter(
    prefix="/auth/gmail",
    tags=["Gmail Authorization"]
)

TOKEN_FILE = Path(__file__).resolve().parents[2] / "gmail_token.json"


@router.get("/login")
async def gmail_login(request: Request):
    redirect_uri = request.url_for("gmail_callback")

    return await oauth.gmail.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline",
        prompt="consent",
        include_granted_scopes="true"
    )


@router.get("/callback", name="gmail_callback")
async def gmail_callback(request: Request):
    try:
        token = await oauth.gmail.authorize_access_token(request)

        user_info = token.get("userinfo")

        if not user_info:
            user_info = await oauth.gmail.userinfo(token=token)

        email = user_info.get("email")

        if not email or user_info.get("email_verified") is not True:
            raise HTTPException(
                status_code=401,
                detail="Gmail account verification failed"
            )

        refresh_token = token.get("refresh_token")

        if not refresh_token:
            raise HTTPException(
                status_code=400,
                detail="Refresh token missing. Please authorize again."
            )

        token_data = {
            "email": email,
            "refresh_token": refresh_token,
            "token_uri": "https://oauth2.googleapis.com/token",
            "scopes": token.get("scope", "")
        }

        temporary_file = TOKEN_FILE.with_suffix(".tmp")

        temporary_file.write_text(
            json.dumps(token_data),
            encoding="utf-8"
        )

        os.replace(temporary_file, TOKEN_FILE)

        return JSONResponse({
            "message": "Gmail authorization successful",
            "email": email
        })

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Gmail authorization failed"
        )
