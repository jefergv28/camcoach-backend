from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.tareas import TareaCreate, TareaUpdate, TareaResponse
from app.crud import tareas as crud_tareas

# 🔑 IMPORTAMOS LA AUTENTICACIÓN Y EL MODELO DE USUARIO
from app.utils.auth import get_current_user
from app.models.usuarios import Usuario

router = APIRouter(
    prefix="/tareas",
    tags=["Planes de Trabajo"]
)

# ==========================================
# 1. CREAR TAREA (Asociada al Admin)
# ==========================================
@router.post("/", response_model=TareaResponse, status_code=status.HTTP_201_CREATED)
def create_tarea(
    tarea: TareaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Candado activado
):
    # Pasamos el id del admin actual para que el CRUD lo guarde en la columna usuario_id
    return crud_tareas.create_tarea(db=db, tarea=tarea, usuario_id=current_user.id)


# ==========================================
# 2. LISTAR TODAS LAS TAREAS DEL ADMIN
# ==========================================
@router.get("/", response_model=List[TareaResponse])
def read_tareas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Candado activado
):
    # 🎯 CORRECCIÓN DEL CRASH: Aquí ya le mandamos el usuario_id que nos exigía el log
    return crud_tareas.get_tareas(db, usuario_id=current_user.id, skip=skip, limit=limit)


# ==========================================
# 3. LISTAR TAREAS DE UN CLIENTE (Protegido)
# ==========================================
@router.get("/cliente/{cliente_id}", response_model=List[TareaResponse])
def read_tareas_por_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Candado activado
):
    # Validamos que las tareas del cliente pertenezcan también a este admin
    return crud_tareas.get_tareas_by_cliente(db, cliente_id=cliente_id, usuario_id=current_user.id)


# ==========================================
# 4. ACTUALIZAR UNA TAREA (Seguro)
# ==========================================
@router.put("/{tarea_id}", response_model=TareaResponse)
def update_tarea(
    tarea_id: int,
    tarea: TareaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Candado activado
):
    # El CRUD validará que la tarea exista Y que pertenezca a este usuario antes de editar
    db_tarea = crud_tareas.update_tarea(db, tarea_id=tarea_id, tarea_data=tarea, usuario_id=current_user.id)
    if db_tarea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada o no tienes autorización para modificarla"
        )
    return db_tarea


# ==========================================
# 5. ELIMINAR UNA TAREA (Seguro)
# ==========================================
@router.delete("/{tarea_id}")
def delete_tarea(
    tarea_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Candado activado
):
    # El CRUD validará la propiedad legítima antes de aplicar el delete físico en PostgreSQL
    db_tarea = crud_tareas.delete_tarea(db, tarea_id=tarea_id, usuario_id=current_user.id)
    if db_tarea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada o no tienes autorización para eliminarla"
        )
    return {"message": "Tarea eliminada exitosamente"}