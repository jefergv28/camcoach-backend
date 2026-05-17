from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.ingresos import IngresoCreate, IngresoUpdate, IngresoResponse
from app.crud import ingresos as crud_ingresos

# 🔑 IMPORTAMOS LA AUTENTICACIÓN Y EL MODELO DE USUARIO
from app.utils.auth import get_current_user
from app.models.usuarios import Usuario

router = APIRouter(
    prefix="/ingresos",
    tags=["Ingresos"]
)

# ==========================================
# 1. REGISTRAR INGRESO (Asociado al Admin)
# ==========================================
@router.post("/", response_model=IngresoResponse, status_code=status.HTTP_201_CREATED)
def create_income(
    ingreso: IngresoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Sesión obligatoria
):
    # Pasamos el id del administrador logueado para marcar la propiedad del dinero
    return crud_ingresos.create_ingreso(
        db=db,
        ingreso=ingreso,
        usuario_id=current_user.id
    )

# ==========================================
# 2. LISTAR INGRESOS (Filtrado por Admin)
# ==========================================
@router.get("/", response_model=List[IngresoResponse])
def read_ingresos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Sesión obligatoria
):
    # El CRUD solo retornará el flujo de caja del administrador actual
    return crud_ingresos.get_ingresos(
        db=db,
        skip=skip,
        limit=limit,
        usuario_id=current_user.id
    )

# ==========================================
# 3. VER UN INGRESO POR ID (Validado)
# ==========================================
@router.get("/{ingreso_id}", response_model=IngresoResponse)
def read_ingreso(
    ingreso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Sesión obligatoria
):
    db_ingreso = crud_ingresos.get_ingreso(
        db=db,
        ingreso_id=ingreso_id,
        usuario_id=current_user.id
    )
    if db_ingreso is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingreso no encontrado o no estás autorizado para consultarlo"
        )
    return db_ingreso

# ==========================================
# 4. MODIFICAR REGISTRO FINANCIERO (Seguro)
# ==========================================
@router.put("/{ingreso_id}", response_model=IngresoResponse)
def update_ingreso(
    ingreso_id: int,
    ingreso: IngresoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Sesión obligatoria
):
    db_ingreso = crud_ingresos.update_ingreso(
        db=db,
        ingreso_id=ingreso_id,
        ingreso_data=ingreso,
        usuario_id=current_user.id
    )
    if db_ingreso is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingreso no encontrado o no tienes permisos de edición"
        )
    return db_ingreso

# ==========================================
# 5. ELIMINAR REGISTRO FINANCIERO (Seguro)
# ==========================================
@router.delete("/{ingreso_id}")
def delete_ingreso(
    ingreso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Sesión obligatoria
):
    db_ingreso = crud_ingresos.delete_ingreso(
        db=db,
        ingreso_id=ingreso_id,
        usuario_id=current_user.id
    )
    if db_ingreso is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingreso no encontrado o no tienes permisos para eliminarlo"
        )
    return {"message": "Ingreso eliminado exitosamente"}