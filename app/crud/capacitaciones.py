from sqlalchemy.orm import Session
from app.models.capacitaciones import Capacitacion
from app.schemas.capacitaciones import CapacitacionCreate, CapacitacionUpdate

# ==========================================
# 1. OBTENER TODAS LAS CAPACITACIONES (Filtrado)
# ==========================================
def get_capacitaciones(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    # 🎯 Clausula filter para traer solo lo que le pertenezca a este admin
    return db.query(Capacitacion).filter(Capacitacion.usuario_id == usuario_id).offset(skip).limit(limit).all()

# ==========================================
# 2. OBTENER UNA CAPACITACIÓN ESPECÍFICA
# ==========================================
def get_capacitacion(db: Session, capacitacion_id: int, usuario_id: int):
    # 🎯 Doble validación: debe coincidir el ID de la capacitación Y el ID del dueño
    return db.query(Capacitacion).filter(
        Capacitacion.id == capacitacion_id,
        Capacitacion.usuario_id == usuario_id
    ).first()

# ==========================================
# 3. CREAR UNA NUEVA CAPACITACIÓN
# ==========================================
def create_capacitacion(db: Session, capacitacion: CapacitacionCreate, usuario_id: int):
    # 🎯 Desestructuramos el esquema e inyectamos de manera explícita el usuario_id dueño
    db_capacitacion = Capacitacion(**capacitacion.dict(), usuario_id=usuario_id)
    db.add(db_capacitacion)
    db.commit()
    db.refresh(db_capacitacion)
    return db_capacitacion

# ==========================================
# 4. ACTUALIZAR CAPACITACIÓN (Seguro)
# ==========================================
def update_capacitacion(db: Session, capacitacion_id: int, capacitacion_data: CapacitacionUpdate, usuario_id: int):
    # 🎯 Primero buscamos asegurando la propiedad del registro
    db_capacitacion = db.query(Capacitacion).filter(
        Capacitacion.id == capacitacion_id,
        Capacitacion.usuario_id == usuario_id
    ).first()

    if db_capacitacion:
        update_data = capacitacion_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_capacitacion, key, value)
        db.commit()
        db.refresh(db_capacitacion)
    return db_capacitacion

# ==========================================
# 5. ELIMINAR CAPACITACIÓN (Seguro)
# ==========================================
def delete_capacitacion(db: Session, capacitacion_id: int, usuario_id: int):
    # 🎯 Buscamos confirmando que el administrador logueado sea el dueño legítimo
    db_capacitacion = db.query(Capacitacion).filter(
        Capacitacion.id == capacitacion_id,
        Capacitacion.usuario_id == usuario_id
    ).first()

    if db_capacitacion:
        db.delete(db_capacitacion)
        db.commit()
    return db_capacitacion