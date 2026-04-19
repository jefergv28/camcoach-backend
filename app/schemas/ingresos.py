from pydantic import BaseModel
from typing import Optional
from datetime import date

class IngresoBase(BaseModel):
    monto: float
    descripcion: Optional[str] = None
    metodo_pago: str
    estado: str
    cliente_id: int
    fecha: Optional[date] = None

class IngresoCreate(IngresoBase):
    pass

class IngresoUpdate(BaseModel):
    monto: Optional[float] = None
    descripcion: Optional[str] = None
    metodo_pago: Optional[str] = None
    estado: Optional[str] = None
    cliente_id: Optional[int] = None

class IngresoResponse(IngresoBase):
    id: int

    class Config:
        orm_mode = True