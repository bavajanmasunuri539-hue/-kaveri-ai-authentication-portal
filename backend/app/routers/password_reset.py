import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import SessionLocal
from app.core.email_service import send_password_reset_email
from app.core.security import get_password_hash
from app.models.user import User
from app.models.password_reset import PasswordResetToken
from app.schemas.password_reset import (
    ForgotPasswordRequest,
    ResetPasswordRequest
)

router = APIRouter(
    prefix="/auth/password",
    tags=["Password Reset"]
)


@router.post("/forgot")
async def forgot_password(data: ForgotPasswordRequest):
    db = SessionLocal()
    email = str(data.email).lower()

    message = {
        "message": "If an account exists for this email, a password reset link will be sent."
    }

    try:
        user = db.query(User).filter(
            User.email == email,
            User.is_active == True
        ).first()

        if not user:
            return message

        raw_token = secrets.token_urlsafe(32)

        token_hash = hashlib.sha256(
            raw_token.encode("utf-8")
        ).hexdigest()

        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id
        ).delete(synchronize_session=False)

        reset_record = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=15)
        )

        db.add(reset_record)
        db.commit()

        frontend_url = os.getenv(
            "FRONTEND_URL",
            "http://localhost:5175"
        ).rstrip("/")

        reset_url = (
            f"{frontend_url}/reset-password?token={quote(raw_token)}"
        )

        try:
            send_password_reset_email(user.email, reset_url)
        except Exception:
            db.delete(reset_record)
            db.commit()

        return message

    except SQLAlchemyError:
        db.rollback()
        return message

    finally:
        db.close()


@router.post("/reset")
async def reset_password(data: ResetPasswordRequest):
    db = SessionLocal()

    try:
        token_hash = hashlib.sha256(
            data.token.encode("utf-8")
        ).hexdigest()

        now = datetime.now(timezone.utc)

        reset_record = db.query(PasswordResetToken).filter(
            PasswordResetToken.token_hash == token_hash
        ).with_for_update().first()

        if (
            not reset_record
            or reset_record.used_at is not None
            or reset_record.expires_at <= now
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid or expired password reset link"
            )

        user = db.query(User).filter(
            User.id == reset_record.user_id,
            User.is_active == True
        ).first()

        if not user:
            raise HTTPException(
                status_code=400,
                detail="Invalid or expired password reset link"
            )

        user.hashed_password = get_password_hash(
            data.new_password
        )

        reset_record.used_at = now

        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.id != reset_record.id
        ).delete(synchronize_session=False)

        db.commit()

        return {
            "message": "Password reset successful. You can now log in."
        }

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Password reset failed"
        )

    finally:
        db.close()
