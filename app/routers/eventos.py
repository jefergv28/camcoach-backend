from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.evento import Evento
from app.models.cliente import Cliente  # Importante para buscar el contacto
from app.schemas.evento import EventoCreate, EventoResponse
# Aquí importarás tus funciones de envío (las que creamos en el paso anterior)
from app.services.notifications import enviar_whatsapp, enviar_correo
from app.services.notifications import enviar_whatsapp, enviar_correo, enviar_sms

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.get("/", response_model=List[EventoResponse])
def obtener_eventos(db: Session = Depends(get_db)):
    return db.query(Evento).all()

@router.post("/", response_model=EventoResponse)
def crear_evento(
    evento: EventoCreate,
    background_tasks: BackgroundTasks, # <--- Inyectamos tareas en segundo plano
    db: Session = Depends(get_db)
):
    # 1. Crear el evento en la DB
    db_evento = Evento(**evento.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)

    # 2. Lógica de Notificación Automática
    if db_evento.notificarCliente:
        # Buscamos los datos de contacto del cliente por su nombre
        cliente_db = db.query(Cliente).filter(Cliente.nombre == db_evento.cliente).first()

        if cliente_db:
            # convertimos el evento a dict para envia a noticaciones
            evento_dict = {
              "titulo":db_evento.titulo,
              "fecha":db_evento.fecha,
              "hora": db_evento.hora,
              "descripcion": db_evento.descripcion,
              "cliente": cliente_db.nombre
            }

            if db_evento.tipoNotifCliente == "whatsapp" and cliente_db.telefono:
                # Se envía a segundo plano para no bloquear la respuesta de la API
                background_tasks.add_task(enviar_whatsapp, cliente_db.telefono, evento_dict)

            elif db_evento.tipoNotifCliente == "sms" and cliente_db.telefono:
                background_tasks.add_task(enviar_sms, cliente_db.telefono, evento_dict)

            elif db_evento.tipoNotifCliente == "email" and cliente_db.email:
                background_tasks.add_task(enviar_correo, cliente_db.email, "Recordatorio de Cita", evento_dict)

    return db_evento

@router.put("/{evento_id}", response_model=EventoResponse)
def actualizar_evento(
    evento_id: int,
    evento_update: EventoCreate,
    background_tasks: BackgroundTasks,  # <-- Agregamos BackgroundTasks
    db: Session = Depends(get_db)
):
    db_evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not db_evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    for key, value in evento_update.dict().items():
        setattr(db_evento, key, value)

    db.commit()
    db.refresh(db_evento)

    # Lógica de notificación al actualizar
    if db_evento.notificarCliente:
     cliente_db = db.query(Cliente).filter(Cliente.nombre == db_evento.cliente).first()
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

@router.delete("/{evento_id}")
def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    db_evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not db_evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    db.delete(db_evento)
    db.commit()
    return {"message": "Evento eliminado correctamente"}