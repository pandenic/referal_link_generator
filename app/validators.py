from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_referral
from app.models import User, ReferralCode


async def check_referral_code_exists(
        user: User,
        session: AsyncSession,
) -> ReferralCode:
    code_obj = await crud_referral.get_by_user(
        user,
        session,
    )
    if code_obj is None:
        raise HTTPException(
            status_code=404,
            detail="Referral code doesn't exists!"
        )
    return code_obj


async def check_referral_code_exists_and_actual(
        code: str,
        session: AsyncSession,
) -> bool:
    code_obj = await crud_referral.get_by_referral_code(
        code,
        session,
    )
    if code_obj is None:
        raise HTTPException(
            status_code=404,
            detail="Referral code doesn't exists!"
        )
    if code_obj.expiration_at < datetime.now():
        raise HTTPException(
            status_code=404,
            detail="Referral code is old!"
        )
    return code_obj
