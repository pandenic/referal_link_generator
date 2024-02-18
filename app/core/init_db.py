"""
Describe action on a DB initialization.

Create async context managers for an async session and a user.
create_user: create a user in DB using context mangers and given data
create_first_superuser: create superuser using data given in settings.
"""

import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.database import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas import UserCreate

get_async_session_context = contextlib.asynccontextmanager(
    get_async_session,
)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: EmailStr,
    password: str,
    is_superuser: bool = False,
):
    """Create a user in DB."""
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(
                    user_db,
                ) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                        ),
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    """Create a superuser with params from settings."""
    if settings.first_superuser_email and settings.first_superuser_password:
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
