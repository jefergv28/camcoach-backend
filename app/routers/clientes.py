from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.usuarios import Usuario
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from app.crud.cliente import (
    create_cliente,
    get_cliente,
    get_clientes,
    update_cliente,
    delete_cliente,
)
from app.utils.auth import get_current_user
from app.utils.logger import registrar_actividad  # 🚀 Tu sistema de logs automáticos

router = APIRouter(prefix="/clientes", tags=["Clientes"])


# ==========================================
# 1. CREAR CLIENTE (Amarrado al Admin Logueado)
# ==========================================
@router.post("/", response_model=ClienteOut, status_code=status.HTTP_201_CREATED)
def create_new_cliente(
    cliente: ClienteCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),  # 🔑 Capturamos el usuario real
):
    # Pasamos el ID del administrador logueado al CRUD
    nuevo_cliente = create_cliente(db, cliente, admin_id=current_user.id)

    # 🚀 Registramos la acción en el historial
    registrar_actividad(
        db=db,
        usuario_id=current_user.id,
        nombre_usuario=current_user.username,
        accion=f"Registró al cliente: {nuevo_cliente.nombre}",
        tipo="creacion",
        request=request,
        detalles=f"Plataforma: {getattr(nuevo_cliente, 'plataforma_principal', 'No registra')}"
    )
    return nuevo_cliente


# ==========================================
# 2. LISTAR CLIENTES (Filtrado por Admin)
# ==========================================
@router.get("/", response_model=List[ClienteOut])
def read_clientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    # Si el que entra no es el admin le cerramos la puerta
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Esta sección es solo para administradores.",
        )

    # 🎯 CORRECCIÓN DEL TYPING ERROR: Pasamos el admin_id que exige tu CRUD blindado
    return get_clientes(db, admin_id=current_user.id, skip=skip, limit=limit)


# ==========================================
# 3. VER UN CLIENTE ESPECÍFICO (Protegido)
# ==========================================
@router.get("/{cliente_id}", response_model=ClienteOut)
def read_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    # 🎯 Buscamos asegurando que pertenezca a este administrador
    db_cliente = get_cliente(db, cliente_id, admin_id=current_user.id)
    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado o no autorizado"
        )
    return db_cliente


# ==========================================
# 4. ACTUALIZAR CLIENTE (Seguro)
# ==========================================
@router.put("/{cliente_id}", response_model=ClienteOut)
def update_existing_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    # 🎯 Actualiza únicamente si el cliente le pertenece al admin logueado
    db_cliente = update_cliente(db, cliente_id, cliente_update, admin_id=current_user.id)
    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado o no autorizado"
        )

    # 🚀 Registramos la edición en el historial
    registrar_actividad(
        db=db,
        usuario_id=current_user.id,
        nombre_usuario=current_user.username,
        accion=f"Actualizó los datos del cliente: {db_cliente.nombre}",
        tipo="edicion",
        request=request,
        detalles=f"Estado actual: {getattr(db_cliente, 'estado', 'N/A')}"
    )
    return db_cliente


# ==========================================
# 5. ELIMINAR CLIENTE (Seguro)
# ==========================================
@router.delete("/{cliente_id}", response_model=ClienteOut)
def delete_existing_cliente(
    cliente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    # 🎯 Elimina únicamente si es el dueño legítimo
    db_cliente = delete_cliente(db, cliente_id, admin_id=current_user.id)
    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado o no autorizado"
        )

    # 🚀 Registramos la eliminación en el historial
    registrar_actividad(
        db=db,
        usuario_id=current_user.id,
        nombre_usuario=current_user.username,
        accion=f"Eliminó del sistema al cliente: {db_cliente.nombre}",
        tipo="eliminacion",
        request=request,
        detalles=f"ID del cliente borrado: {cliente_id}"
    )
    return db_cliente