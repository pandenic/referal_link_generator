from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    path: str

    app_title: str = 'Referral link creator'
    secret: str = 'SECRET'

    db_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/db'

    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    referral_link_length: int = 16

    class Config:
        """
        Configure parameters in settings.

        env_file: a path to an env file
        """

        env_file = '.env'
        extra = 'allow'


settings = Settings()
