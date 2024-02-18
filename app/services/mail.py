"""Describes services for mail processing."""
from email.mime.text import MIMEText
from smtplib import SMTP
from ssl import create_default_context

from app.core.config import settings


def send_referral_code(
    referral_code: str,
    referrer_mail: str,
):
    """Send a referral code by mail."""
    message = MIMEText("Your referral code: " + referral_code, "html")
    message["From"] = settings.mail_username
    message["To"] = referrer_mail
    message["Subject"] = "Your referral code"

    ctx = create_default_context()

    try:
        with SMTP(settings.mail_host, settings.mail_port) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(settings.mail_username, settings.mail_password)
            server.send_message(message)
            server.quit()
        return {"status": 200, "errors": None}
    except Exception as error:
        return {"status": 500, "errors": error}
