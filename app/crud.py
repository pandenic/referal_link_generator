from datetime import datetime
from typing import TypeVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.models import User
from app.services.referral import generate_referral_code, calculate_end_date

ModelType = TypeVar('ModelType', bound=Base)


class CRUDReferral():

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def commit_and_refresh(
            self,
            session: AsyncSession,
            user: User,
    ):
        session.add(user)
        await session.commit()
        await session.refresh(user)

    async def new_referral_code(
            self,
            session: AsyncSession,
            user: User,
            referral_lifetime_days: int,
    ):
        user.referral_code = generate_referral_code()
        user.referral_created_at = datetime.now()
        user.referral_expiration_at = calculate_end_date(
            user.referral_created_at,
            referral_lifetime_days,
        )
        await self.commit_and_refresh(session, user)
        return user

    async def delete_referral_code(
            self,
            session: AsyncSession,
            user: User,
    ):
        user.referral_code = None
        user.referral_created_at = None
        user.referral_expiration_at = None
        return self.commit_and_refresh(session, user)


crud_referral = CRUDReferral(User)

