from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from . import models
from sqlalchemy.orm import Session

async def send_magic_link(email: str, token: str, db: Session):
    # Prendi un account email valido dal DB (esempio: il primo)
    email_account = db.query(models.EmailAccount).order_by(models.EmailAccount.id.desc()).first()

    if not email_account:
        raise Exception("Nessun account email configurato")

    print(email_account.email_from)

    conf = ConnectionConfig(
        MAIL_USERNAME=email_account.smtp_username,
        MAIL_PASSWORD=email_account.smtp_password,
        MAIL_FROM=email_account.email_from,
        MAIL_PORT=email_account.smtp_port,
        MAIL_SERVER=email_account.smtp_server,
        MAIL_STARTTLS=email_account.smtp_starttls,
        MAIL_SSL_TLS=email_account.smtp_ssl_tls,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )

    message = MessageSchema(
        subject="Il tuo link di login",
        recipients=[email],
        body=f"Token di accesso: {token}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
