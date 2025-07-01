from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from .config import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

security = HTTPBearer()

def generate_token(email: str) -> str:
    return serializer.dumps(email, salt="passwordless-login")

def verify_token(token: str, max_age: int = 600) -> str:
    try:
        email = serializer.loads(token, salt="passwordless-login", max_age=max_age)
        return email
    except SignatureExpired:
        raise ValueError("Token scaduto")
    except BadSignature:
        raise ValueError("Token non valido")
    
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token non valido")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token non valido")
