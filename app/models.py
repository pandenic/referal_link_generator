from datetime import datetime
from typing import Optional, Set, List
from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.core.database import Base

class ReferralCode(Base):
    referrer_id: Mapped[UUID] = mapped_column(
        ForeignKey('user.id'),
        primary_key=True,
    )
    code: Mapped[Optional[str]]
    created_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now,
    )
    expiration_at: Mapped[Optional[datetime]]


class User(SQLAlchemyBaseUserTableUUID, Base):
    """Contain User model description."""
    referrer_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey('user.id'),
    )
    referrer: Mapped[Optional["User"]] = relationship(
        back_populates="referrals",
        remote_side="User.id",
    )
    referrals: Mapped[Optional["User"]] = relationship(
        back_populates="referrer",
    )

