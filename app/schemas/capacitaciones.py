from pydantic import BaseModel
from typing import Optional
from enum import Enum

class TipoCapacitacion(str, Enum):
    video = "video"
    presentacion = "presentacion"
    documento = "documento"

class EstadoCapacitacion(str, Enum):
    disponible = "disponible"
    proximamente = "proximamente"

class CapacitacionBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    tipo: TipoCapacitacion
    url: Optional[str] = None
    estado: EstadoCapacitacion = EstadoCapacitacion.disponible

class CapacitacionCreate(CapacitacionBase):
    pass

class CapacitacionUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[TipoCapacitacion] = None
    url: Optional[str] = None
    estado: Optional[EstadoCapacitacion] = None

class CapacitacionResponse(CapacitacionBase):
    id: int

    class Config:
        orm_mode = True