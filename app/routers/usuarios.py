"""
Router de gestión de usuarios y permisos.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.usuarios import Usuario, RolUsuario
from app.schemas.usuarios import UsuarioCreate, UsuarioResponse
from app.crud import usuarios as crud_usuarios
from app.utils.auth import get_current_user, get_current_user_optional
from app.utils.security import obtener_hash_password

router = APIRouter(prefix="/usuarios", tags=["Usuarios y Permisos"])


# -------------------------
# RESET PASSWORD SCHEMA
# -------------------------
class ResetPasswordRequest(BaseModel):
    new_password: str


# -------------------------
# LISTAR USUARIOS
# -------------------------
@router.get("/", response_model=List[UsuarioResponse])
def read_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    # ADMIN ve solo los usuarios que creó
    if current_user.rol == RolUsuario.admin:
        return (
            db.query(Usuario)
            .filter(Usuario.admin_id == current_user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # CLIENTE solo se ve a sí mismo
    return [current_user]


# -------------------------
# CREAR USUARIO
# -------------------------
@router.post("/", response_model=UsuarioResponse)
def create_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_optional),
):
    # 1. evitar duplicados
    db_user = crud_usuarios.get_usuario_by_email(db, email=usuario.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # 2. primer usuario => ADMIN
    if current_user is None:
        return crud_usuarios.create_usuario(
            db=db,
            usuario=usuario,
            rol=RolUsuario.admin,
            admin_id=None,
        )

    # 3. admin crea cliente
    if current_user.rol == RolUsuario.admin:
        return crud_usuarios.create_usuario(
            db=db,
            usuario=usuario,
            rol=RolUsuario.cliente,
            admin_id=current_user.id,
        )

    # 4. cliente no puede crear usuarios
    raise HTTPException(
        status_code=403,
        detail="No tienes permisos para crear usuarios",
    )


# -------------------------
# RESET PASSWORD
# -------------------------
@router.put("/{usuario_id}/reset-password")
def reset_password(
    usuario_id: int,
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    db_usuario = (
        db.query(Usuario)
        .filter(
            Usuario.id == usuario_id,
            Usuario.admin_id == current_user.id
        )
        .first()
    )

    if not db_usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado o no autorizado"
        )

    db_usuario.hashed_password = obtener_hash_password(payload.new_password)
    db.commit()

    return {"message": "Contraseña actualizada exitosamente"}


# -------------------------
# DELETE USUARIO
# -------------------------
@router.delete("/{usuario_id}")
def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    db_usuario = (
        db.query(Usuario)
        .filter(
            Usuario.id == usuario_id,
            Usuario.admin_id == current_user.id
        )
        .first()
    )

    if not db_usuario:
        raise HTTPException(
            status_code=404,
            detail="No tienes permiso para eliminar este usuario"
        )

    db.delete(db_usuario)
    db.commit()

    return {"message": "Usuario eliminado exitosamente"}