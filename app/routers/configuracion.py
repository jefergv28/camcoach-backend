from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuarios import Usuario
from app.utils.auth import get_current_user
from app.schemas.configuracion import ConfiguracionSchema
from app.crud import configuracion as crud_config

router = APIRouter(prefix="/configuracion", tags=["Configuración del Sistema"])


@router.get("/", response_model=ConfiguracionSchema)
def obtener_configuracion(
    db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)
):
    """
    Trae la configuración completa del usuario logueado usando su sesión.
    """
    return crud_config.get_configuracion_usuario(db, usuario_id=current_user.id)


@router.put("/", response_model=ConfiguracionSchema)
def guardar_configuracion(
    payload: ConfiguracionSchema,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Guarda los cambios aplicados en el formulario de configuración.
    """

    return crud_config.update_configuracion_usuario(
        db, usuario_id=current_user.id, data=payload.dict()
    )
