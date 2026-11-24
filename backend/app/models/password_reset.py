from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.core.database import Base


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    token_hash = Column(
        String(255),
        unique=True,
        nullable=False
    )

    expires_at = Column(DateTime(timezone=True), nullable=False)

    used_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
