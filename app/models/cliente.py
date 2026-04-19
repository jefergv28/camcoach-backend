from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from datetime import datetime
from app.database import Base
import enum

class EstadoCliente(str, enum.Enum):
    activa = "activa"
    pausada = "pausada"

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=True)
    whatsapp = Column(String, nullable=True)
    plataforma_principal = Column(String, nullable=False)
    estado = Column(Enum(EstadoCliente), default=EstadoCliente.activa, nullable=False)
    ingresos_mes = Column(Float, default=0.0)
    fecha_union = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Cliente {self.nombre} - {self.estado}>"