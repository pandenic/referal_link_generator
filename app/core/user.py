"""Initialization and settigs for FastAPI Users."""
from typing import Optional, Union
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers,
                           InvalidPasswordException, UUIDIDMixin, models,
                           schemas)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_async_session
from app.models import User
from app.schemas import ReferrerIdUserCreate, UserCreate
from app.validators import check_referral_code_exists_and_valid


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Create a db session with SQLAlchemyUserDatabase adapted."""
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """Set JWT strategy for FastAPI Users."""
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    """User management logic."""

    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        OVERRIDE to process referral code on user creation.

        Create a user in database.
        """
        referral_code = user_create.__dict__.get("referral_code")
        if referral_code is not None:
            code_obj = await check_referral_code_exists_and_valid(
                referral_code,
                self.user_db.session,
            )
            create_dict = user_create.dict()
            if not create_dict.get("referral_code"):
                raise ValueError("Wrong user pydantic schema.")
            create_dict.pop("referral_code")
            create_dict["referrer_id"] = code_obj.referrer_id
            user_create = ReferrerIdUserCreate(**create_dict)

        return await super().create(user_create, safe, request)

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Validate password from request."""
        if len(password) < 3:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters",
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail",
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None,
    ):
        """Actions after User registrations."""
        print(f"User {user.id} has registered.") # noqa


async def get_user_manager(user_db=Depends(get_user_db)):
    """Get user manager and bind int to db session."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
