from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from .database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class InviteCode(Base):
    __tablename__ = "invite_codes"
    code = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    used = Column(Boolean, default=False)
    max_uses = Column(Integer, default=1)
    use_count = Column(Integer, default=0)

class EmailAccount(Base):
    __tablename__ = "email_accounts"
    id = Column(Integer, primary_key=True, index=True)
    email_from = Column(String, unique=True, index=True)
    smtp_username = Column(String)
    smtp_password = Column(String)
    smtp_server = Column(String)
    smtp_port = Column(Integer)
    smtp_starttls = Column(Boolean, default=True)
    smtp_ssl_tls = Column(Boolean, default=False)

