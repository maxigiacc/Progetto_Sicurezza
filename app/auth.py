from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from .config import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from .config import settings

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Non usato direttamente, ma serve per FastAPI

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Credenziali non valide")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token non valido")


def generate_token(email: str) -> str:
    return serializer.dumps(email, salt="passwordless-login")

def verify_token(token: str, max_age: int = 240) -> str:
    try:
        email = serializer.loads(token, salt="passwordless-login", max_age=max_age)
        return email
    except SignatureExpired:
        raise ValueError("Token scaduto")
    except BadSignature:
        raise ValueError("Token non valido")