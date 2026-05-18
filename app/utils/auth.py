from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from fastapi import Cookie, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuarios import Usuario
from app.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# 🎯 Esquema estándar para leer el Header 'Authorization: Bearer <token>'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

# =========================
# CREAR TOKEN
# =========================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


# =========================
# USUARIO OBLIGATORIO (BLINDADO)
# =========================
async def get_current_user(
    request: Request,
    header_token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    # 🎯 INTELIGENCIA DE EXTRACCIÓN:
    # 1. Intentamos leer desde el Header (Bearer)
    token = header_token

    # 2. Si no hay header, intentamos leer desde las cookies ("token" o "camcoach_token")
    if not token:
        token = request.cookies.get("token") or request.cookies.get("camcoach_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se encontró un token de sesión válido en los encabezados ni en las cookies.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except (JWTError, ValidationError):
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.email == email).first()

    if user is None:
        raise credentials_exception

    return user


# =========================
# USUARIO OPCIONAL (BLINDADO)
# =========================
async def get_current_user_optional(
    request: Request,
    header_token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    token = header_token

    if not token:
        token = request.cookies.get("token") or request.cookies.get("camcoach_token")

    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            return None

        user = db.query(Usuario).filter(Usuario.email == email).first()
        return user

    except (JWTError, ValidationError):
        return None