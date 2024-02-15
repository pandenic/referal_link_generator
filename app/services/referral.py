import secrets
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from smtplib import SMTP
from ssl import create_default_context

from app.core.config import settings


def generate_referral_code() -> str:
    return secrets.token_urlsafe(settings.referral_link_length)


def calculate_end_date(start_date: datetime, interval_in_days: int) -> datetime:
    return start_date + timedelta(days=interval_in_days)


def send_referral_code(
        referral_code: str,
        referrer_mail: str,
):
    message = MIMEText("Your referral code: " + referral_code, "html")
    message["From"] = settings.mail_username
    message["To"] = referrer_mail
    message["Subject"] = "Your referral code"

    ctx = create_default_context()

    try:
        with SMTP(
                settings.mail_host,
                settings.mail_port
        ) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(
                settings.mail_username,
                settings.mail_password
            )
            server.send_message(message)
            server.quit()
        return {
            "status": 200,
            "errors": None
        }
    except Exception as error:
        return {
            "status": 500,
            "errors": error
        }