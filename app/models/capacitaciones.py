from sqlalchemy import Column, Integer, String, Enum as SQLEnum
import enum
from app.database import Base
class TipoCapacitacion(str, enum.Enum):
    video = "video"
    presentacion = "presentacion"
    documento = "documento"

class EstadoCapacitacion(str, enum.Enum):
    disponible = "disponible"
    proximamente = "proximamente"

class Capacitacion(Base):
    __tablename__ = "capacitaciones"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)
    descripcion = Column(String, nullable=True)
    tipo = Column(SQLEnum(TipoCapacitacion), default=TipoCapacitacion.video)
    url = Column(String, nullable=True) # Puede ser null si el estado es "proximamente"
    estado = Column(SQLEnum(EstadoCapacitacion), default=EstadoCapacitacion.disponible)