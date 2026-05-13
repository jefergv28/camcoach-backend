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

    todos_los_usuarios = db.query(Usuario).all()
    print(f"🕵️ DETECTIVE: Hay {len(todos_los_usuarios)} usuarios en la BD.")
    for u in todos_los_usuarios:
        print(f"   -> Correo guardado: '{u.email}' (Estado: Activo={u.is_active})")

    user = db.query(Usuario).filter(Usuario.email == email_ingresado).first()

    if not user:
        print("❌ ERROR: El correo NO coincidió con ninguno de la lista de arriba.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verificar_password(form_data.password, user.hashed_password):
        print("❌ ERROR: La contraseña no coincide con el hash guardado.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print("✅ LOGIN EXITOSO. Generando token...")

    access_token = create_access_token(data={"sub": user.email})

    response.set_cookie(
        key="camcoach_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600 * 24,
        path="/",
        domain="localhost",
    )

    return {"access_token": access_token, "token_type": "bearer"}


# <--- Cambiamos UserOut por UsuarioResponse
@router.get("/me", response_model=UsuarioResponse)
def get_current_user_info(
    current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Devuelve los datos del usuario actualmente logueado.
    Requiere token válido (en cookie o header).
    """
    user = db.query(Usuario).filter(Usuario.email == current_user.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return user
