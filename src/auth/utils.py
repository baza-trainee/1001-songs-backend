from fastapi_mail import FastMail, MessageSchema
from fastapi_users.password import PasswordHelper
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.config import mail_config, settings
from .exceptions import EMAIL_BODY


def add_user_data(email: str, password: str, session: AsyncSession):
    instance = User(
        email=email,
        hashed_password=PasswordHelper().hash(password),
        is_superuser=True,
        is_active=True,
        is_verified=True,
    )
    session.add(instance)


async def send_reset_email(email: str, token: str):
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[
            email,
        ],
        body=EMAIL_BODY % (settings.BASE_URL, token),
        subtype="html",
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
