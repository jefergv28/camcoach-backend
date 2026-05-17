from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.historial import Historial
from app.models.usuarios import Usuario
from app.utils.auth import get_current_user

router = APIRouter(prefix="/historial", tags=["Historial de Actividad"])

# ==========================================
# LISTAR HISTORIAL (Aislamiento Multi-Tenant)
# ==========================================
@router.get("/")
def obtener_historial(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Retorna el historial de actividad limitando el alcance al usuario logueado.
    Evita que los administradores espíen las acciones de otros administradores.
    """
    # 🎯 EL CANDADO DEFINITIVO: Tanto para admin como para clientes independientes,
    # filtramos estrictamente por su propio ID de usuario logueado.
    registros = (
        db.query(Historial)
        .filter(Historial.usuario_id == current_user.id)
        .order_by(Historial.fecha.desc())
        .limit(50)
        .all()
    )

    # Mapeamos los datos al formato exacto que espera tu frontend
    resultado = []
    for r in registros:
        resultado.append({
            "id": r.id,
            "usuario": r.nombre_usuario,
            "accion": r.accion,
            "tipo": r.tipo,
            "fecha": r.fecha.isoformat() if hasattr(r.fecha, "isoformat") else str(r.fecha),
            "ip": r.ip or "Desconocida",
            "detalles": r.detalles or ""
        })

    return resultado