from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.user import get_user_by_email
from app.schemas.auth import Token, TokenData
from app.utils.auth import create_access_token, get_current_user
from app.config import settings
from app.schemas.auth import UserOut  # Asegúrate de importar UserOut aquí

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
def login(
    response: Response,
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
    print("Seteando cookie: camcoach_token con valor:", access_token[:20] + "...")  # Debug

    response.set_cookie(
        key="camcoach_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600 * 24,
        path="/",
        domain="localhost"
    )

    return {"access_token": access_token, "token_type": "bearer"}

# <--- Aquí exactamente va el nuevo endpoint /me
@router.get("/me", response_model=UserOut)
def get_current_user_info(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Devuelve los datos del usuario actualmente logueado.
    Requiere token válido (en cookie o header).
    """
    user = get_user_by_email(db, current_user.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user