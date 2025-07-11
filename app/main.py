from fastapi import FastAPI, Depends, HTTPException, Request, Security
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from jose import jwt
from datetime import datetime, timedelta
import secrets

from . import models, mailer, auth
from .database import SessionLocal, engine
from .config import settings
from .auth import get_current_user

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia con i tuoi domini specifici
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB and limiter setup
models.Base.metadata.create_all(bind=engine)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# API key setup
API_KEY = "SUPERSEGRETO"
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Accesso negato")
    return api_key

# Error handling
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Troppi tentativi, riprova più tardi."})

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT creation
def create_access_token(user: models.User, expires_delta: timedelta | None = None):
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode = {
        "sub": user.email,
        "exp": expire,
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Endpoints
@app.post("/request-invite")
async def request_invite(data: models.InviteRequest, db: Session = Depends(get_db)):
    invite_code = secrets.token_urlsafe(32)
    invite = models.InviteCode(code=invite_code, max_uses=1, use_count=0)
    db.add(invite)
    db.commit()
    await mailer.send_invite_code(data.email, invite_code, db)
    return {"msg": "Codice di invito inviato via email"}

@app.post("/register")
def register_user(data: models.RegisterRequest, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Utente già registrato")
    invite = db.query(models.InviteCode).filter(models.InviteCode.code == data.code).first()
    if not invite or invite.used or invite.use_count >= invite.max_uses:
        raise HTTPException(status_code=400, detail="Codice invito non valido o usato")
    db.add(models.User(email=data.email))
    invite.use_count += 1
    if invite.use_count >= invite.max_uses:
        invite.used = True
    db.commit()
    return {"msg": "Registrazione avvenuta con successo"}

@app.post("/login")
@limiter.limit("5/minute")
async def login_request(data: models.LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utente non registrato")
    token = auth.generate_token(data.email)
    await mailer.send_magic_link(data.email, token, db)
    return {"msg": "Link inviato"}

@app.get("/verify")
def verify_token(token: str, db: Session = Depends(get_db)):
    try:
        email = auth.verify_token(token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    
    access_token = create_access_token(user, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(user_email: str = Depends(get_current_user)):
    return {"msg": f"Benvenuto, {user_email}! Sei nella sezione protetta."}


