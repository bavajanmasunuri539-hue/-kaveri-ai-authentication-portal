from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.database import SessionLocal
from app.core.security import get_password_hash, verify_password
from app.core.jwt import create_access_token
from app.models.user import User
from app.schemas.email_auth import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth/email", tags=["Email Authentication"])


def create_auth_response(user: User, message: str):
    access_token = create_access_token({
        "sub": user.email,
        "user_id": user.id
    })

    response = JSONResponse({
        "message": message,
        "authenticated": True,
        "user": {
            "id": user.id,
            "email": user.email
        }
    })

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


@router.post("/register")
async def register(data: RegisterRequest):
    db = SessionLocal()
    email = str(data.email).lower()

    try:
        existing_user = db.query(User).filter(
            func.lower(User.email) == email
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email address is already registered"
            )

        user = User(
            email=email,
            hashed_password=get_password_hash(data.password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return create_auth_response(
            user,
            "Account registered successfully"
        )

    except HTTPException:
        db.rollback()
        raise

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email address is already registered"
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

    finally:
        db.close()


@router.post("/login")
async def login(data: LoginRequest):
    db = SessionLocal()
    email = str(data.email).lower()

    try:
        user = db.query(User).filter(
            func.lower(User.email) == email
        ).first()

        if not user or not user.hashed_password:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="This account is inactive"
            )

        return create_auth_response(
            user,
            "Login successful"
        )

    except HTTPException:
        raise

    finally:
        db.close()
