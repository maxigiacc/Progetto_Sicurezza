from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from . import models, database, mailer, auth
from .database import SessionLocal, engine
from .config import settings
from fastapi.responses import JSONResponse, HTMLResponse
from jose import jwt
from datetime import datetime, timedelta
import uuid

from .auth import get_current_user
from pydantic import BaseModel, EmailStr

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # porta del tuo frontend React
    # aggiungi altri origin se serve
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # o ["*"] per permettere tutti (solo in sviluppo)
    allow_credentials=True,
    allow_methods=["*"],    # permette GET, POST, OPTIONS, PUT, DELETE ecc.
    allow_headers=["*"],
)

class RegisterRequest(BaseModel):
    email: str
    code: str

class LoginRequest(BaseModel):
    email: EmailStr


models.Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Troppi tentativi, riprova più tardi."},
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@app.post("/login")
@limiter.limit("5/minute")
async def login_request(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    email = data.email
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utente non registrato")

    token = auth.generate_token(email)
    await mailer.send_magic_link(email, token, db)  # PASSA il db

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

    # Genera JWT dopo verifica token magic link
    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(user_email: str = Depends(get_current_user)):
    return {"msg": f"Benvenuto, {user_email}! Sei nella sezione protetta."}

@app.post("/admin/invite")
def generate_invite_code(max_uses: int = 1, db: Session = Depends(get_db)):
    code = str(uuid.uuid4())
    invite = models.InviteCode(code=code, max_uses=max_uses)
    db.add(invite)
    db.commit()
    return {"invite_code": code}

@app.post("/register")
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    email = data.email
    code = data.code

    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Utente già registrato")

    invite = db.query(models.InviteCode).filter(models.InviteCode.code == code).first()
    if not invite:
        raise HTTPException(status_code=400, detail="Codice invito non valido")
    
    if invite.used or invite.use_count >= invite.max_uses:
        raise HTTPException(status_code=400, detail="Codice già usato o scaduto")

    # Crea utente
    user = models.User(email=email)
    db.add(user)

    # Aggiorna invito
    invite.use_count += 1
    if invite.use_count >= invite.max_uses:
        invite.used = True

    db.commit()
    return {"msg": "Registrazione avvenuta con successo"}



from pydantic import BaseModel

class EmailAccountCreate(BaseModel):
    email_from: str
    smtp_username: str
    smtp_password: str
    smtp_server: str
    smtp_port: int
    smtp_starttls: bool = True
    smtp_ssl_tls: bool = False


from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException

API_KEY = "SUPERSEGRETO"
API_KEY_NAME = "Authorization"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Accesso negato")
    return api_key

@app.post("/admin/email_account")
def add_email_account(data: EmailAccountCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    existing = db.query(models.EmailAccount).filter(models.EmailAccount.email_from == data.email_from).first()
    if existing:
        raise HTTPException(status_code=400, detail="Account email già esistente")

    new_account = models.EmailAccount(
        email_from=data.email_from,
        smtp_username=data.smtp_username,
        smtp_password=data.smtp_password,
        smtp_server=data.smtp_server,
        smtp_port=data.smtp_port,
        smtp_starttls=data.smtp_starttls,
        smtp_ssl_tls=data.smtp_ssl_tls,
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return {"msg": "Account email aggiunto", "id": new_account.id}
