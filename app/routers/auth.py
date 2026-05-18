from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuarios import Usuario
from app.schemas.auth import Token, TokenData
from app.utils.auth import create_access_token, get_current_user
from app.config import settings
from app.schemas.usuarios import UsuarioResponse
from app.utils.security import verificar_password

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    email_ingresado = form_data.username.strip()
    print(f"🛑 INTENTO DE LOGIN: Buscando -> '{email_ingresado}'")

    user = db.query(Usuario).filter(Usuario.email == email_ingresado).first()

    if not user or not verificar_password(form_data.password, user.hashed_password):
        print("❌ ERROR: Credenciales inválidas.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print("✅ LOGIN EXITOSO. Generando token...")
    access_token = create_access_token(data={"sub": user.email})

    # 🎯 CORRECCIÓN 1: Eliminamos 'domain=localhost' y ajustamos las banderas para producción
    # Al quitar 'domain', la cookie se asocia automáticamente al dominio real donde corre la API (Local o Render)
    response.set_cookie(
        key="token",  # 🔄 Sincronizado con el nombre "token" que usa tu Frontend
        value=access_token,
        httponly=False,       # Permite que js-cookie en Vercel lo lea sin líos de CORS
        secure=True,          # OBLIGATORIO para HTTPS en producción
        samesite="none",      # Permite transferencia cross-origin entre Vercel y Render
        max_age=3600 * 24,
        path="/",
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UsuarioResponse)
def get_current_user_info(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Devuelve los datos del usuario actualmente logueado.
    Garantiza compatibilidad leyendo la base de datos a través del payload validado por get_current_user.
    """
    # 🎯 CORRECCIÓN 2: Aseguramos la búsqueda usando el atributo de email del token decodificado
    email_token = getattr(current_user, "email", None) or getattr(current_user, "username", None) or current_user.sub

    user = db.query(Usuario).filter(Usuario.email == email_token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado en el sistema"
        )
    return user