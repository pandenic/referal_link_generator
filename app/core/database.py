from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declared_attr, declarative_base

from app.core.config import settings


class PreBase:
    """
    Declare attributes for each table in DB.

    __tablename__ == model class name
    id: unique id field
    """

    @declared_attr
    def __tablename__(cls):
        """Bind table name to the class name."""
        return cls.__name__.lower()


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.postgres_connection_url)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
