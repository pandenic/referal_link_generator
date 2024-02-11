from datetime import datetime
from typing import TypeVar, Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped

from app.core.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """Contain User model description."""

    referral_code: Mapped[Optional[str]]
    referral_created_at: Mapped[Optional[datetime]]
    referral_expiration_at:  Mapped[Optional[datetime]]
