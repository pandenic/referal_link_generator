"""Settings for a FastAPI app."""
from typing import Optional

from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    """FastAPI settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_title: str = "Referral link creator"
    secret: str = "SECRET"

    db_name: str
    db_username: str
    db_password: SecretStr
    db_host: str
    db_port: int

    redis_name: str
    redis_username: str
    redis_password: SecretStr
    redis_host: str
    redis_port: int

    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    referral_link_length: int = 16

    mail_host: Optional[str] = None
    mail_username: Optional[EmailStr] = None
    mail_password: Optional[str] = None
    mail_port: Optional[str] = None

    @property
    def postgres_connection_url(self) -> URL:
        """Return URL for connections establishing to postgres."""
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db_username,
            password=self.db_password.get_secret_value(),
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

    @property
    def redis_connection_url(self) -> URL:
        """Return URL for connections establishing to redis."""
        return URL.create(
            drivername="redis",
            password=self.redis_password.get_secret_value(),
            host=self.redis_host,
            port=self.redis_port,
            database=self.redis_name,
            query={
                "socket_keepalive": "True",
            },
        )


settings = Settings()
