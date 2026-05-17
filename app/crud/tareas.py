from sqlalchemy.orm import Session
from app.models.tareas import Tarea
from app.schemas.tareas import TareaCreate, TareaUpdate

# ==========================================
# 1. OBTENER TODAS LAS TAREAS DEL ADMIN
# ==========================================
def get_tareas(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    # 🎯 EL CANDADO: Filtra para traer solo los pendientes de este administrador
    return db.query(Tarea).filter(Tarea.usuario_id == usuario_id).offset(skip).limit(limit).all()

# ==========================================
# 2. OBTENER TAREAS DE UN CLIENTE ESPECÍFICO
# ==========================================
def get_tareas_by_cliente(db: Session, cliente_id: int, usuario_id: int):
    # 🎯 DOBLE CANDADO: Que pertenezcan al cliente Y al administrador logueado
    return db.query(Tarea).filter(
        Tarea.cliente_id == cliente_id,
        Tarea.usuario_id == usuario_id
    ).all()

# ==========================================
# 3. OBTENER UNA TAREA POR ID (Validada)
# ==========================================
def get_tarea(db: Session, tarea_id: int, usuario_id: int):
    # 🎯 DOBLE CANDADO: Verifica que exista el ID y que sea el dueño legítimo
    return db.query(Tarea).filter(
        Tarea.id == tarea_id,
        Tarea.usuario_id == usuario_id
    ).first()

# ==========================================
# 4. CREAR UNA NUEVA TAREA
# ==========================================
def create_tarea(db: Session, tarea: TareaCreate, usuario_id: int):
    # 🎯 Inyectamos explícitamente el usuario_id al desempaquetar el esquema
    db_tarea = Tarea(**tarea.dict(), usuario_id=usuario_id)
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

# ==========================================
# 5. ACTUALIZAR UNA TAREA (Seguro)
# ==========================================
def update_tarea(db: Session, tarea_id: int, tarea_data: TareaUpdate, usuario_id: int):
    # 🎯 Buscamos asegurando primero la propiedad de la tarea antes de modificarla
    db_tarea = db.query(Tarea).filter(
        Tarea.id == tarea_id,
        Tarea.usuario_id == usuario_id
    ).first()

    if db_tarea:
        update_data = tarea_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tarea, key, value)
        db.commit()
        db.refresh(db_tarea)
    return db_tarea

# ==========================================
# 6. ELIMINAR UNA TAREA (Seguro)
# ==========================================
def delete_tarea(db: Session, tarea_id: int, usuario_id: int):
    # 🎯 Buscamos confirmando que el administrador actual sea el dueño
    db_tarea = db.query(Tarea).filter(
        Tarea.id == tarea_id,
        Tarea.usuario_id == usuario_id
    ).first()

    if db_tarea:
        db.delete(db_tarea)
        db.commit()
    return db_tarea