from sqlalchemy.orm import Session
from app.models.tareas import Tarea
from app.schemas.tareas import TareaCreate, TareaUpdate

def get_tareas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tarea).offset(skip).limit(limit).all()

def get_tareas_by_cliente(db: Session, cliente_id: int):
    return db.query(Tarea).filter(Tarea.cliente_id == cliente_id).all()

def get_tarea(db: Session, tarea_id: int):
    return db.query(Tarea).filter(Tarea.id == tarea_id).first()

def create_tarea(db: Session, tarea: TareaCreate):
    db_tarea = Tarea(**tarea.dict())
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

def update_tarea(db: Session, tarea_id: int, tarea_data: TareaUpdate):
    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if db_tarea:
        update_data = tarea_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tarea, key, value)
        db.commit()
        db.refresh(db_tarea)
    return db_tarea

def delete_tarea(db: Session, tarea_id: int):
    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if db_tarea:
        db.delete(db_tarea)
        db.commit()
    return db_tarea