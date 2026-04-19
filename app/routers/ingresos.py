from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.ingresos import IngresoCreate, IngresoUpdate, IngresoResponse
from app.crud import ingresos as crud_ingresos

router = APIRouter(
    prefix="/ingresos",
    tags=["Ingresos"]
)

@router.post("/", response_model=IngresoResponse)
def create_ingreso(ingreso: IngresoCreate, db: Session = Depends(get_db)):
    return crud_ingresos.create_ingreso(db=db, ingreso=ingreso)

@router.get("/", response_model=List[IngresoResponse])
def read_ingresos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_ingresos.get_ingresos(db, skip=skip, limit=limit)

@router.get("/{ingreso_id}", response_model=IngresoResponse)
def read_ingreso(ingreso_id: int, db: Session = Depends(get_db)):
    db_ingreso = crud_ingresos.get_ingreso(db, ingreso_id=ingreso_id)
    if db_ingreso is None:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")
    return db_ingreso

@router.put("/{ingreso_id}", response_model=IngresoResponse)
def update_ingreso(ingreso_id: int, ingreso: IngresoUpdate, db: Session = Depends(get_db)):
    db_ingreso = crud_ingresos.update_ingreso(db, ingreso_id, ingreso)
    if db_ingreso is None:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")
    return db_ingreso

@router.delete("/{ingreso_id}")
def delete_ingreso(ingreso_id: int, db: Session = Depends(get_db)):
    db_ingreso = crud_ingresos.delete_ingreso(db, ingreso_id)
    if db_ingreso is None:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")
    return {"message": "Ingreso eliminado exitosamente"}