import pickle
from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Response, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.core.redis import redis_client
from app.validators import check_referral_code_exists
from app.core.database import get_async_session
from app.core.user import current_user
from app.crud import crud_referral, crud_user
from app.models import User, ReferralCode
from app.schemas import ReferralCodeCreate, ReferralCodeRead, UserRead
from app.services.referral import send_referral_code

router = APIRouter()


@router.post(
    '/',
    response_model=ReferralCodeRead,
    dependencies=[Depends(current_user)],
)
async def create_referral_code(
    referral_code_lifetime: ReferralCodeCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> ReferralCode:
    code_obj = await crud_referral.get_by_user(
        user, session
    )
    if code_obj:
        code_obj = await crud_referral.update(
            code_obj,
            referral_code_lifetime.lifetime,
            session,
        )
    else:
        code_obj = await crud_referral.create(
            user,
            referral_code_lifetime.lifetime,
            session,
        )
    return code_obj


@router.delete(
    '/',
    response_model=ReferralCodeRead,
    dependencies=[Depends(current_user)],
)
async def delete_referral_code(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> ReferralCode:
    code_obj = await check_referral_code_exists(
        user, session
    )
    await crud_referral.remove(code_obj, session)
    return code_obj


@router.post(
    '/mail-referral-code',
    dependencies=[Depends(current_user)],
)
async def mail_referral_code(
    task: BackgroundTasks,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    code_obj = await check_referral_code_exists(
        user, session
    )
    task.add_task(
        send_referral_code,
        code_obj.code,
        user.email,
    )
    return JSONResponse(content={
        "message": f"Referral code have been sent to {user.email}."
    }, status_code=HTTPStatus.OK)


@router.get(
    '/{referrer_id}',
    response_model=List[UserRead],
    dependencies=[Depends(current_user)],
)
async def get_referrals(
    referrer_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    return await crud_user.get_referrals_by_referrer_id(
        referrer_id,
        session,
    )

