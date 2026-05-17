from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.capacitaciones import (
    CapacitacionCreate,
    CapacitacionUpdate,
    CapacitacionResponse,
)
from app.crud import capacitaciones as crud_capacitaciones

# 🔑 IMPORTAMOS LA AUTENTICACIÓN Y EL MODELO DE USUARIO
from app.utils.auth import get_current_user
from app.models.usuarios import Usuario

router = APIRouter(prefix="/capacitaciones", tags=["Capacitaciones"])


# ==========================================
# 1. CREAR CAPACITACIÓN (Amarrada al Admin)
# ==========================================
@router.post(
    "/", response_model=CapacitacionResponse, status_code=status.HTTP_201_CREATED
)
def create_capacitacion(
    capacitacion: CapacitacionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),  # 🔐 Seguridad activada
):
    # Pasamos el id del administrador para que el CRUD lo asigne como dueño
    return crud_capacitaciones.create_capacitacion(
        db=db, capacitacion=capacitacion, usuario_id=current_user.id
    )


# ==========================================
# 2. LISTAR CAPACITACIONES (Filtradas)
# ==========================================
@router.get("/", response_model=List[CapacitacionResponse])
def read_capacitaciones(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),  # 🔐 Seguridad activada
):
    # Filtramos la lista para que solo devuelva las de este administrador
    return crud_capacitaciones.get_capacitaciones(
        db=db, skip=skip, limit=limit, usuario_id=current_user.id
    )


# ==========================================
# 3. VER UNA CAPACITACIÓN POR ID (Protegido)
# ==========================================
@router.get("/{capacitacion_id}", response_model=CapacitacionResponse)
def read_capacitacion(
    capacitacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),  # 🔐 Seguridad activada
):
    # El CRUD debe buscar por ID del registro Y por ID del usuario dueño
    db_capacitacion = crud_capacitaciones.get_capacitacion(
        db=db, capacitacion_id=capacitacion_id, usuario_id=current_user.id
    )
    if db_capacitacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Capatitación no encontrada o no tienes permisos para verla",
        )
    return db_capacitacion


# ==========================================
# 4. ACTUALIZAR CAPACITACIÓN (Protegido)
# ==========================================
@router.put("/{capacitacion_id}", response_model=CapacitacionResponse)
def update_capacitacion(
    capacitacion_id: int,
    capacitacion: CapacitacionUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),  # 🔐 Seguridad activada
):
    db_capacitacion = crud_capacitaciones.update_capacitacion(
        db=db,
        capacitacion_id=capacitacion_id,
        capacitacion_data=capacitacion,
        usuario_id=current_user.id,
    )
    if db_capacitacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Capacitación no encontrada o no tienes permisos para modificarla",
        )
    return db_capacitacion


# ==========================================
# 5. ELIMINAR CAPACITACIÓN (Protegido)
# ==========================================
@router.delete("/{capacitacion_id}")
def delete_capacitacion(
    capacitacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),  # 🔐 Seguridad activada
):
    db_capacitacion = crud_capacitaciones.delete_capacitacion(
        db=db, capacitacion_id=capacitacion_id, usuario_id=current_user.id
    )
    if db_capacitacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Capacitación no encontrada o no tienes permisos para eliminarla",
        )
    return {"message": "Capacitación eliminada exitosamente"}
