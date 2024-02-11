import secrets
from datetime import datetime, timedelta

from app.core.config import settings


def generate_referral_code() -> str:
    return secrets.token_urlsafe(settings.referral_link_length)


def calculate_end_date(start_date: datetime, interval_in_days: int) -> datetime:
    return start_date + timedelta(days=interval_in_days)
