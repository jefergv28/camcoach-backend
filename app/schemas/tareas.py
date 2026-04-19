from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class EstadoTarea(str, Enum):
    pendiente = "pendiente"
    progreso = "progreso"
    completado = "completado"

class PrioridadTarea(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"

class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    estado: EstadoTarea = EstadoTarea.pendiente
    prioridad: PrioridadTarea = PrioridadTarea.media
    fecha_limite: Optional[date] = None
    cliente_id: int

class TareaCreate(TareaBase):
    pass

class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[EstadoTarea] = None
    prioridad: Optional[PrioridadTarea] = None
    fecha_limite: Optional[date] = None
    cliente_id: Optional[int] = None

class TareaResponse(TareaBase):
    id: int

    class Config:
        orm_mode = True