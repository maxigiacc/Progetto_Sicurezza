from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from sqlalchemy.orm import Session
from . import models

from .config import settings

async def send_magic_link(email: str, token: str, db: Session):

    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.EMAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )

    message = MessageSchema(
        subject="Token di accesso",
        recipients=[email],
        body=f"Usa questo token per accedere: {token}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

async def send_invite_code(email: str, code: str, db: Session):

    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.EMAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )

    message = MessageSchema(
        subject="Codice di invito al servizio",
        recipients=[email],
        body=f"<p>Il tuo codice di invito è: <strong> {code}</strong></p>",
        subtype = MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
