import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    EMAIL_FROM = os.getenv("EMAIL_FROM")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    # app/config.py
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 5


settings = Settings()
