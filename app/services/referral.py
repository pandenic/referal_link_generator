"""Describes services for referral code generations."""
import secrets
from datetime import datetime, timedelta

from app.core.config import settings


def generate_referral_code() -> str:
    """Generate a valid and urlsafe referral code."""
    return secrets.token_urlsafe(settings.referral_link_length)


def calculate_end_date(
    start_date: datetime, interval_in_days: int,
) -> datetime:
    """Calculate an expiration date."""
    return start_date + timedelta(seconds=interval_in_days)
