"""CRUD class description for ReferralCode model."""
import pickle
from datetime import datetime
from typing import Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.core.redis import (delete_referral_redis, get_referral_redis,
                            set_referral_redis)
from app.models import ReferralCode, User
from app.services.referral import calculate_end_date, generate_referral_code

ModelType = TypeVar("ModelType", bound=Base)


class CRUDReferral:
    """CRUD class for Referral model."""

    def __init__(self, model: Type[ModelType]):
        """Init for CRUDReferral class."""
        self.model = model

    async def get_redis_by_field(
        self,
        session: AsyncSession,
        model_field,
        value,
    ):
        """
        Get certain ReferralCode model obj.

        from redis cache or postgres database
        by referral code or user
        update or set it to redis cache
        """
        if referral_code := await get_referral_redis(value):
            return pickle.loads(referral_code)
        db_obj = await session.execute(
            select(self.model).where(
                model_field == value,
            ),
        )
        db_obj = db_obj.scalars().first()
        if db_obj:
            await set_referral_redis(db_obj)
        return db_obj

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        """
        Get certain ReferralCode model obj.

        from redis cache or postgres database
        by user
        update or set it to redis cache
        """
        return await self.get_redis_by_field(
            session, self.model.referrer_id, user.id,
        )

    async def get_by_referral_code(
        self,
        code: str,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        """
        Get certain ReferralCode model obj.

        from redis cache or postgres database
        by referral code
        update or set it to redis cache
        """
        return await self.get_redis_by_field(
            session,
            self.model.code,
            code,
        )

    async def update(
        self,
        db_obj: ModelType,
        lifetime: int,
        session: AsyncSession,
    ) -> ModelType:
        """
        Update certain ReferralCode model obj.

        with certain lifetime
        update result in redis cache
        """
        await delete_referral_redis(db_obj)
        db_obj.created_at = datetime.now()
        db_obj.code = generate_referral_code()
        db_obj.expiration_at = calculate_end_date(db_obj.created_at, lifetime)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        await set_referral_redis(db_obj)
        return db_obj

    async def create(
        self,
        user: User,
        lifetime: int,
        session: AsyncSession,
    ) -> ModelType:
        """
        Create ReferralCode model obj.

        with certain lifetime
        for certain user
        adds result to redis cache
        """
        created_time = datetime.now()
        obj_data = {
            "referrer_id": user.id,
            "code": generate_referral_code(),
            "created_at": created_time,
            "expiration_at": calculate_end_date(
                created_time,
                lifetime,
            ),
        }
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        await set_referral_redis(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """
        Remove certain ReferralCode model obj.

        from postgres database
        from redis cache
        """
        await delete_referral_redis(db_obj)
        await session.delete(db_obj)
        await session.commit()
        await delete_referral_redis(db_obj)
        return db_obj


crud_referral = CRUDReferral(ReferralCode)
