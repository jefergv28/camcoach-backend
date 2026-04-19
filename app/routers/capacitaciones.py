from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.capacitaciones import CapacitacionCreate, CapacitacionUpdate, CapacitacionResponse
from app.crud import capacitaciones as crud_capacitaciones

router = APIRouter(
    prefix="/capacitaciones",
    tags=["Capacitaciones"]
)

@router.post("/", response_model=CapacitacionResponse)
def create_capacitacion(capacitacion: CapacitacionCreate, db: Session = Depends(get_db)):
    return crud_capacitaciones.create_capacitacion(db=db, capacitacion=capacitacion)

@router.get("/", response_model=List[CapacitacionResponse])
def read_capacitaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_capacitaciones.get_capacitaciones(db, skip=skip, limit=limit)

@router.get("/{capacitacion_id}", response_model=CapacitacionResponse)
def read_capacitacion(capacitacion_id: int, db: Session = Depends(get_db)):
    db_capacitacion = crud_capacitaciones.get_capacitacion(db, capacitacion_id=capacitacion_id)
    if db_capacitacion is None:
        raise HTTPException(status_code=404, detail="Capacitación no encontrada")
    return db_capacitacion

@router.put("/{capacitacion_id}", response_model=CapacitacionResponse)
def update_capacitacion(capacitacion_id: int, capacitacion: CapacitacionUpdate, db: Session = Depends(get_db)):
    db_capacitacion = crud_capacitaciones.update_capacitacion(db, capacitacion_id, capacitacion)
    if db_capacitacion is None:
        raise HTTPException(status_code=404, detail="Capacitación no encontrada")
    return db_capacitacion

@router.delete("/{capacitacion_id}")
def delete_capacitacion(capacitacion_id: int, db: Session = Depends(get_db)):
    db_capacitacion = crud_capacitaciones.delete_capacitacion(db, capacitacion_id)
    if db_capacitacion is None:
        raise HTTPException(status_code=404, detail="Capacitación no encontrada")
    return {"message": "Capacitación eliminada exitosamente"}