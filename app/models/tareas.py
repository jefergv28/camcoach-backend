from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum as SQLEnum
import enum
from app.database import Base


class EstadoTarea(str, enum.Enum):
    pendiente = "pendiente"
    progreso = "progreso"
    completado = "completado"

class PrioridadTarea(str, enum.Enum):
    baja = "baja"
    media = "media"
    alta = "alta"

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(SQLEnum(EstadoTarea), default=EstadoTarea.pendiente)
    prioridad = Column(SQLEnum(PrioridadTarea), default=PrioridadTarea.media)
    fecha_limite = Column(Date, nullable=True)

    # Llave foránea conectando al cliente
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)