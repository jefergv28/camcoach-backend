from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.models.configuracion import Configuracion

def get_configuracion_usuario(db: Session, usuario_id: int) -> dict:
    user = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    config = db.query(Configuracion).filter(Configuracion.usuario_id == usuario_id).first()

    # Si no tiene configuración creada, se la generamos de una vez
    if not config:
        config = Configuracion(usuario_id=usuario_id)
        db.add(config)
        db.commit()
        db.refresh(config)

    return {
        "nombre": user.username,
        "email": user.email,
        "telefono": config.telefono,
        "notificaciones": {
            "email": config.notif_email,
            "whatsapp": config.notif_whatsapp,
            "app": config.notif_app
        },
        "idioma": config.idioma
    }

def update_configuracion_usuario(db: Session, usuario_id: int, data: dict) -> dict:
    user = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    config = db.query(Configuracion).filter(Configuracion.usuario_id == usuario_id).first()

    if not config:
        config = Configuracion(usuario_id=usuario_id)
        db.add(config)

    # 1. Actualizamos datos primarios del Usuario
    user.username = data.get("nombre", user.username)
    user.email = data.get("email", user.email)

    # 2. Actualizamos preferencias
    config.telefono = data.get("telefono", config.telefono)
    config.idioma = data.get("idioma", config.idioma)

    # 3. Desglosamos el objeto de notificaciones del Frontend
    notif = data.get("notificaciones", {})
    if "email" in notif: config.notif_email = notif["email"]
    if "whatsapp" in notif: config.notif_whatsapp = notif["whatsapp"]
    if "app" in notif: config.notif_app = notif["app"]

    db.commit()
    return get_configuracion_usuario(db, usuario_id)