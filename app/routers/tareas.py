from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.tareas import TareaCreate, TareaUpdate, TareaResponse
from app.crud import tareas as crud_tareas

router = APIRouter(
    prefix="/tareas",
    tags=["Planes de Trabajo"]
)

@router.post("/", response_model=TareaResponse)
def create_tarea(tarea: TareaCreate, db: Session = Depends(get_db)):
    return crud_tareas.create_tarea(db=db, tarea=tarea)

@router.get("/", response_model=List[TareaResponse])
def read_tareas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_tareas.get_tareas(db, skip=skip, limit=limit)

@router.get("/cliente/{cliente_id}", response_model=List[TareaResponse])
def read_tareas_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return crud_tareas.get_tareas_by_cliente(db, cliente_id=cliente_id)

@router.put("/{tarea_id}", response_model=TareaResponse)
def update_tarea(tarea_id: int, tarea: TareaUpdate, db: Session = Depends(get_db)):
    db_tarea = crud_tareas.update_tarea(db, tarea_id, tarea)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

@router.delete("/{tarea_id}")
def delete_tarea(tarea_id: int, db: Session = Depends(get_db)):
    db_tarea = crud_tareas.delete_tarea(db, tarea_id)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada exitosamente"}
