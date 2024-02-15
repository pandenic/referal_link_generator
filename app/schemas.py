from datetime import datetime
from typing import TypeVar, Optional
from uuid import UUID

from fastapi_users import schemas
from pydantic import BaseModel, Extra, Field, field_validator, ValidationInfo, ConfigDict, PrivateAttr

from app.models import User


class ReferralCodeCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    lifetime: int = Field(30, gt=0)


class ReferralCodeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    referrer_id: Optional[UUID] = None
    code: Optional[str] = None
    created_at: Optional[datetime] = None
    expiration_at: Optional[datetime] = None


class UserRead(schemas.BaseUser[UUID], ReferralCodeRead):
    """Default fastapi_users.schemas Read class."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Default fastapi_users.schemas Create class."""
    referral_code: Optional[str] = None


class ReferrerIdUserCreate(schemas.BaseUserCreate):
    """Default fastapi_users.schemas Create class."""
    referrer_id: Optional[UUID]


class UserUpdate(schemas.BaseUserUpdate):
    """Default fastapi_users.schemas Update class."""
    pass
