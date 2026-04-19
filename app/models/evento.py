from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    fecha = Column(String, nullable=False)  # Guardamos como string ISO para match con el front
    hora = Column(String, nullable=True)
    cliente = Column(String, nullable=False) # Nombre del cliente (como lo tienes en el front)
    descripcion = Column(String, nullable=True)
    miRecordatorio = Column(Boolean, default=False)
    notificarCliente = Column(Boolean, default=False)
    tipoNotifCliente = Column(String, nullable=True) # "whatsapp" | "email" | "sms"

    def __repr__(self):
        return f"<Evento {self.titulo} - {self.cliente}>"