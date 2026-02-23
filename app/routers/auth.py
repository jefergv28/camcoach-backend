from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.user import get_user_by_email
from app.schemas.auth import Token
from app.utils.auth import create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
def login(
    response: Response,  # Agregamos Response para setear cookies
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    print("Seteando cookie: camcoach_token con valor:", access_token[:20] + "...")  # Debug: ver en terminal

    # Setear cookie httpOnly
    response.set_cookie(
        key="camcoach_token",
        value=access_token,
        httponly=True,           # No accesible desde JS → más seguro
       secure=False,
    samesite="lax",  # o "none" para pruebas estrictas
    max_age=3600 * 24,  # 24 horas
    path="/",
    domain="localhost"  # ← Agrega esto explícitamente
    )

    return {"access_token": access_token, "token_type": "bearer"}  # Seguimos retornando el token por si lo necesitas en frontend