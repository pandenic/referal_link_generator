from datetime import datetime
from typing import TypeVar, Type, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.models import User, ReferralCode
from app.services.referral import generate_referral_code, calculate_end_date

ModelType = TypeVar('ModelType', bound=Base)


class CRUDReferral():

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.referrer_id == user.id,
            )
        )
        return db_obj.scalars().first()

    async def get_by_referral_code(
            self,
            code: str,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.code == code,
            )
        )
        return db_obj.scalars().first()

    async def update(
            self,
            db_obj: ModelType,
            lifetime: int,
            session: AsyncSession,
    ) -> ModelType:
        db_obj.created_at = datetime.now()
        db_obj.code = generate_referral_code()
        db_obj.expiration_at = calculate_end_date(
            db_obj.created_at,
            lifetime
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def create(
            self,
            user: User,
            lifetime: int,
            session: AsyncSession,
    ) -> ModelType:
        created_time = datetime.now()
        obj_data = {
            "referrer_id": user.id,
            "code": generate_referral_code(),
            "created_at": created_time,
            "expiration_at": calculate_end_date(
                created_time,
                lifetime,
            )
        }
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj


crud_referral = CRUDReferral(ReferralCode)
