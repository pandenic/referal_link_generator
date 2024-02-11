from datetime import datetime
from typing import TypeVar, Optional
from uuid import UUID

from fastapi_users import schemas
from pydantic import BaseModel, Extra, Field


class ReferralCodeCreate(BaseModel):
    lifetime: int = Field(30, gt=0)

    class Config:
        """Schema config."""

        extra = Extra.forbid


class ReferralCodeRead(BaseModel):
    referral_code: Optional[str]
    referral_created_at: Optional[datetime]
    referral_expiration_at: Optional[datetime]


class UserRead(schemas.BaseUser[UUID], ReferralCodeRead):
    """Default fastapi_users.schemas Read class."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Default fastapi_users.schemas Create class."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Default fastapi_users.schemas Update class."""
    pass
