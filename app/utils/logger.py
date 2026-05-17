from sqlalchemy.orm import Session
from fastapi import Request
from app.models.historial import Historial

def registrar_actividad(
    db: Session,
    usuario_id: int,
    nombre_usuario: str,
    accion: str,
    tipo: str,
    request: Request,
    detalles: str = None
):
    """
    Guarda de forma automática una acción en la tabla de historial.
    Captura la IP real del cliente desde la petición de FastAPI.
    """
    try:
        # Capturamos la IP real (si está detrás de un proxy como Nginx saca X-Forwarded-For, si no, la directa)
        ip_cliente = request.headers.get("X-Forwarded-For") or (request.client.host if request.client else "127.0.0.1")

        nueva_actividad = Historial(
            usuario_id=usuario_id,
            nombre_usuario=nombre_usuario,
            accion=accion,
            tipo=tipo,
            ip=ip_cliente,
            detalles=detalles
        )
        db.add(nueva_actividad)
        db.commit()
        db.refresh(nueva_actividad)
        return nueva_actividad
    except Exception as e:
        # Si falla el historial por alguna razón, hacemos rollback para no trabar la acción principal
        db.rollback()
        print(f"⚠️ Error no crítico al registrar en historial: {e}")
        return None