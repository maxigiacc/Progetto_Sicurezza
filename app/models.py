from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from .database import Base
import uuid
from pydantic import BaseModel, EmailStr


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

# Schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    code: str

class LoginRequest(BaseModel):
    email: EmailStr

class InviteRequest(BaseModel):
    email: EmailStr
