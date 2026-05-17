from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.evento import Evento
from app.models.cliente import Cliente
from app.models.usuarios import Usuario
from app.schemas.evento import EventoCreate, EventoResponse
from app.utils.auth import get_current_user

# Funciones de envío en segundo plano
from app.services.notifications import enviar_whatsapp, enviar_correo, enviar_sms

router = APIRouter(prefix="/eventos", tags=["Eventos"])

# ==========================================
# 1. LISTAR EVENTOS (Aislamiento Total)
# ==========================================
@router.get("/", response_model=List[EventoResponse])
def obtener_eventos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Capturamos la sesión
):
    # 🎯 EL CANDADO: Trae solo los eventos del administrador que tiene la sesión abierta
    return db.query(Evento).filter(Evento.usuario_id == current_user.id).all()


# ==========================================
# 2. CREAR EVENTO (Amarrado al Admin + Notificación Segura)
# ==========================================
@router.post("/", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
def crear_evento(
    evento: EventoCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Capturamos la sesión
):
    # 1. Crear el evento en la DB inyectando el ID del administrador dueño
    db_evento = Evento(**evento.dict(), usuario_id=current_user.id)
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)

    # 2. Lógica de Notificación Automática (Blindada)
    if db_evento.notificarCliente:
        # 🎯 FILTRO INTEGRADO: Buscamos el contacto asegurando que pertenezca al ADMIN actual
        cliente_db = db.query(Cliente).filter(
            Cliente.nombre == db_evento.cliente,
            Cliente.admin_id == current_user.id
        ).first()

        if cliente_db:
            evento_dict = {
                "titulo": db_evento.titulo,
                "fecha": db_evento.fecha,
                "hora": db_evento.hora,
                "descripcion": db_evento.descripcion,
                "cliente": cliente_db.nombre
            }

            if db_evento.tipoNotifCliente == "whatsapp" and cliente_db.telefono:
                background_tasks.add_task(enviar_whatsapp, cliente_db.telefono, evento_dict)

            elif db_evento.tipoNotifCliente == "sms" and cliente_db.telefono:
                background_tasks.add_task(enviar_sms, cliente_db.telefono, evento_dict)

            elif db_evento.tipoNotifCliente == "email" and cliente_db.email:
                background_tasks.add_task(enviar_correo, cliente_db.email, "Recordatorio de Cita", evento_dict)

    return db_evento


# ==========================================
# 3. ACTUALIZAR EVENTO (Validación de Propiedad)
# ==========================================
@router.put("/{evento_id}", response_model=EventoResponse)
def actualizar_evento(
    evento_id: int,
    evento_update: EventoCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Capturamos la sesión
):
    # 🎯 VALIDACIÓN: El evento debe existir Y pertenecer al administrador logueado
    db_evento = db.query(Evento).filter(
        Evento.id == evento_id,
        Evento.usuario_id == current_user.id
    ).first()

    if not db_evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado o no tienes permisos para modificarlo"
        )

    for key, value in evento_update.dict().items():
        setattr(db_evento, key, value)

    db.commit()
    db.refresh(db_evento)

    # Lógica de notificación al actualizar
    if db_evento.notificarCliente:
        # Buscamos el cliente validando su pertenencia al admin
        cliente_db = db.query(Cliente).filter(
            Cliente.nombre == db_evento.cliente,
            Cliente.admin_id == current_user.id
        ).first()

        if cliente_db:
            evento_dict = {
                "titulo": db_evento.titulo,
                "fecha": db_evento.fecha,
                "hora": db_evento.hora,
                "descripcion": db_evento.descripcion,
                "cliente": cliente_db.nombre
            }

            if db_evento.tipoNotifCliente == "whatsapp" and cliente_db.telefono:
                background_tasks.add_task(enviar_whatsapp, cliente_db.telefono, evento_dict)

            elif db_evento.tipoNotifCliente == "sms" and cliente_db.telefono:
                background_tasks.add_task(enviar_sms, cliente_db.telefono, evento_dict)

            elif db_evento.tipoNotifCliente == "email" and cliente_db.email:
                background_tasks.add_task(enviar_correo, cliente_db.email, "Actualización de Cita", evento_dict)

    return db_evento


# ==========================================
# 4. ELIMINAR EVENTO (Validación de Propiedad)
# ==========================================
@router.delete("/{evento_id}")
def eliminar_evento(
    evento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # 🔐 Capturamos la sesión
):
    # 🎯 VALIDACIÓN: Solo se puede borrar si es dueño del registro
    db_evento = db.query(Evento).filter(
        Evento.id == evento_id,
        Evento.usuario_id == current_user.id
    ).first()

    if not db_evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado o no tienes permisos para eliminarlo"
        )

    db.delete(db_evento)
    db.commit()
    return {"message": "Evento eliminado correctamente"}