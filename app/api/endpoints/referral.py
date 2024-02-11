from http import HTTPStatus

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.user import current_user
from app.crud import crud_referral
from app.models import User
from app.schemas import ReferralCodeCreate, ReferralCodeRead

router = APIRouter()


@router.post(
    '/',
    response_model=ReferralCodeRead,
    dependencies=[Depends(current_user)],
)
async def create_referral_code(
    referral_code: ReferralCodeCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    user = await crud_referral.new_referral_code(
        session=session,
        user=user,
        referral_lifetime_days=referral_code.lifetime,
    )
    return user


@router.delete(
    '/',
    dependencies=[Depends(current_user)],
)
async def delete_referral_code(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    await crud_referral.delete_referral_code(
        session=session,
        user=user,
    )
    return Response(status_code=HTTPStatus.OK)
