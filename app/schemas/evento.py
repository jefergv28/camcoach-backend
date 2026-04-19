from pydantic import BaseModel
from typing import Optional

class EventoBase(BaseModel):
    titulo: str
    fecha: str
    hora: Optional[str] = None
    cliente: str
    descripcion: Optional[str] = None
    miRecordatorio: bool = False
    notificarCliente: bool = False
    tipoNotifCliente: Optional[str] = "whatsapp"

class EventoCreate(EventoBase):
    pass

class EventoResponse(EventoBase):
    id: int

    class Config:
        from_attributes = True # Esto permite que Pydantic lea modelos de SQLAlchemy