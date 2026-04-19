from sqlalchemy.orm import Session
from app.models.ingresos import Ingreso
from app.schemas.ingresos import IngresoCreate, IngresoUpdate

def get_ingresos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ingreso).offset(skip).limit(limit).all()

def get_ingreso(db: Session, ingreso_id: int):
    return db.query(Ingreso).filter(Ingreso.id == ingreso_id).first()

def create_ingreso(db: Session, ingreso: IngresoCreate):
    db_ingreso = Ingreso(**ingreso.dict())
    db.add(db_ingreso)
    db.commit()
    db.refresh(db_ingreso)
    return db_ingreso

def update_ingreso(db: Session, ingreso_id: int, ingreso_data: IngresoUpdate):
    db_ingreso = db.query(Ingreso).filter(Ingreso.id == ingreso_id).first()
    if db_ingreso:
        update_data = ingreso_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ingreso, key, value)
        db.commit()
        db.refresh(db_ingreso)
    return db_ingreso

def delete_ingreso(db: Session, ingreso_id: int):
    db_ingreso = db.query(Ingreso).filter(Ingreso.id == ingreso_id).first()
    if db_ingreso:
        db.delete(db_ingreso)
        db.commit()
    return db_ingreso