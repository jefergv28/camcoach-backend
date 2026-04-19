from sqlalchemy.orm import Session
from app.models.capacitaciones import Capacitacion
from app.schemas.capacitaciones import CapacitacionCreate, CapacitacionUpdate

def get_capacitaciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Capacitacion).offset(skip).limit(limit).all()

def get_capacitacion(db: Session, capacitacion_id: int):
    return db.query(Capacitacion).filter(Capacitacion.id == capacitacion_id).first()

def create_capacitacion(db: Session, capacitacion: CapacitacionCreate):
    db_capacitacion = Capacitacion(**capacitacion.dict())
    db.add(db_capacitacion)
    db.commit()
    db.refresh(db_capacitacion)
    return db_capacitacion

def update_capacitacion(db: Session, capacitacion_id: int, capacitacion_data: CapacitacionUpdate):
    db_capacitacion = db.query(Capacitacion).filter(Capacitacion.id == capacitacion_id).first()
    if db_capacitacion:
        update_data = capacitacion_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_capacitacion, key, value)
        db.commit()
        db.refresh(db_capacitacion)
    return db_capacitacion

def delete_capacitacion(db: Session, capacitacion_id: int):
    db_capacitacion = db.query(Capacitacion).filter(Capacitacion.id == capacitacion_id).first()
    if db_capacitacion:
        db.delete(db_capacitacion)
        db.commit()
    return db_capacitacion