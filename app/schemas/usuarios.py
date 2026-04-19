from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RolUsuario(str, Enum):
    admin = "admin"
    cliente = "cliente"

class UsuarioBase(BaseModel):
    username: str
    email: EmailStr
    rol: RolUsuario = RolUsuario.cliente
    is_active: bool = True
    cliente_id: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    password: str # El usuario envía la contraseña en texto plano al crearse

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    rol: Optional[RolUsuario] = None
    is_active: Optional[bool] = None
    cliente_id: Optional[int] = None

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True