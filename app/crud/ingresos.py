from sqlalchemy.orm import Session
from app.models.ingresos import Ingreso
from app.schemas.ingresos import IngresoCreate, IngresoUpdate

# ==========================================
# 1. OBTENER INGRESOS DE UN ADMIN (Filtrado)
# ==========================================
def get_ingresos(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    # 🎯 EL CANDADO: Trae solo la caja que le pertenece a este usuario
    return db.query(Ingreso).filter(Ingreso.usuario_id == usuario_id).offset(skip).limit(limit).all()

# ==========================================
# 2. OBTENER UN INGRESO ESPECÍFICO (Validado)
# ==========================================
def get_ingreso(db: Session, ingreso_id: int, usuario_id: int):
    # 🎯 DOBLE CANDADO: El ID del registro debe existir Y pertenecer al admin logueado
    return db.query(Ingreso).filter(
        Ingreso.id == ingreso_id,
        Ingreso.usuario_id == usuario_id
    ).first()

# ==========================================
# 3. REGISTRAR UN NUEVO INGRESO
# ==========================================
def create_ingreso(db: Session, ingreso: IngresoCreate, usuario_id: int):
    # 🎯 Inyectamos explícitamente el usuario_id al desestructurar el esquema
    db_ingreso = Ingreso(**ingreso.dict(), usuario_id=usuario_id)
    db.add(db_ingreso)
    db.commit()
    db.refresh(db_ingreso)
    return db_ingreso

# ==========================================
# 4. ACTUALIZAR UN INGRESO (Seguro)
# ==========================================
def update_ingreso(db: Session, ingreso_id: int, ingreso_data: IngresoUpdate, usuario_id: int):
    # 🎯 Buscamos asegurando primero la propiedad del registro financiero
    db_ingreso = db.query(Ingreso).filter(
        Ingreso.id == ingreso_id,
        Ingreso.usuario_id == usuario_id
    ).first()

    if db_ingreso:
        update_data = ingreso_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ingreso, key, value)
        db.commit()
        db.refresh(db_ingreso)
    return db_ingreso

# ==========================================
# 5. ELIMINAR UN INGRESO (Seguro)
# ==========================================
def delete_ingreso(db: Session, ingreso_id: int, usuario_id: int):
    # 🎯 Buscamos confirmando que el administrador logueado sea el dueño legítimo de la factura
    db_ingreso = db.query(Ingreso).filter(
        Ingreso.id == ingreso_id,
        Ingreso.usuario_id == usuario_id
    ).first()

    if db_ingreso:
        db.delete(db_ingreso)
        db.commit()
    return db_ingreso