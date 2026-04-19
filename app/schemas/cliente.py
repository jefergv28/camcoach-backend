from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class EstadoCliente(str, Enum):
    activa = "activa"
    pausada = "pausada"

class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    email: EmailStr
    telefono: Optional[str] = None
    whatsapp: Optional[str] = None
    plataforma_principal: str = Field(..., min_length=3)
    estado: EstadoCliente = EstadoCliente.activa
    ingresos_mes: float = Field(0.0, ge=0.0)

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    whatsapp: Optional[str] = None
    plataforma_principal: Optional[str] = None
    estado: Optional[EstadoCliente] = None
    ingresos_mes: Optional[float] = None

class ClienteOut(ClienteBase):
    id: int
    fecha_union: datetime

    class Config:
        from_attributes = True