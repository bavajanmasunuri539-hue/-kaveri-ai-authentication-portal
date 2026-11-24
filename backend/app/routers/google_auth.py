import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.oauth import oauth
from app.core.database import SessionLocal
from app.core.jwt import create_access_token, verify_access_token
from app.models.user import User

router = APIRouter(prefix="/auth/google", tags=["Google Authentication"])

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5174")


@router.get("/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback", name="google_callback")
async def google_callback(request: Request):
    db = SessionLocal()

    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")

        if not user_info:
            raise HTTPException(status_code=401, detail="Google user information could not be verified")

        google_sub = user_info.get("sub")
        email = user_info.get("email")
        email_verified = user_info.get("email_verified")

        if not google_sub or not email or email_verified is not True:
            raise HTTPException(status_code=401, detail="Google email verification failed")

        user = db.query(User).filter(User.google_sub == google_sub).first()

        if not user:
            user = db.query(User).filter(User.email == email).first()

            if user:
                if user.google_sub and user.google_sub != google_sub:
                    raise HTTPException(status_code=409, detail="Google account does not match this email")
                user.google_sub = google_sub
            else:
                user = User(email=email, google_sub=google_sub, hashed_password=None)
                db.add(user)

            db.commit()
            db.refresh(user)

        if not user.is_active:
            raise HTTPException(status_code=403, detail="This account is inactive")

        access_token = create_access_token({
            "sub": user.email,
            "user_id": user.id
        })

        response = RedirectResponse(
            url=f"{FRONTEND_URL}/",
            status_code=303
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=1800,
            path="/"
        )

        return response

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed")

    except Exception:
        db.rollback()
        raise HTTPException(status_code=401, detail="Google authentication failed")

    finally:
        db.close()


@router.get("/me")
async def get_current_user(request: Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = verify_access_token(access_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found or inactive")

        return {
            "authenticated": True,
            "user": {
                "id": user.id,
                "email": user.email
            }
        }

    finally:
        db.close()

@router.post("/logout")
async def logout():
    response = JSONResponse({
        "message": "Logged out successfully"
    })

    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )

    return response