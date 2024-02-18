"""CRUD class description for User model."""
from typing import Optional, Type
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.referral import ModelType
from app.models import User


class CRUDUser:
    """CRUD class for User model."""

    def __init__(self, model: Type[ModelType]):
        """Init for CRUDUser class."""
        self.model = model

    async def get_referrals_by_referrer_id(
        self,
        referrer_id: UUID,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        """Get referrals from model by referrer id."""
        referrals = await session.execute(
            select(self.model).where(self.model.referrer_id == referrer_id),
        )
        return referrals.scalars().all()


crud_user = CRUDUser(User)
