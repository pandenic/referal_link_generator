"""Describes SQLAlchemy User model."""
from typing import Optional
from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """Contains User model description."""

    referrer_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("user.id"),
    )
    referrer: Mapped[Optional["User"]] = relationship(
        back_populates="referrals",
        remote_side="User.id",
    )
    referrals: Mapped[Optional["User"]] = relationship(
        back_populates="referrer",
    )
