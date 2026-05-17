from pydantic import BaseModel, EmailStr

class NotificacionesSchema(BaseModel):
    email: bool
    whatsapp: bool
    app: bool

    class Config:
        from_attributes = True

class ConfiguracionSchema(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str | None = None
    notificaciones: NotificacionesSchema
    idioma: str

    class Config:
        from_attributes = True