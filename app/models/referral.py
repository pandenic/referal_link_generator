"""Describes SQLAlchemy Referral code model."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ReferralCode(Base):
    """Contains Referral code model description."""

    referrer_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id"),
        primary_key=True,
    )
    code: Mapped[Optional[str]]
    created_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now,
    )
    expiration_at: Mapped[Optional[datetime]]
