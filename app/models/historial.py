from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Historial(Base):
    __tablename__ = "historial"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    nombre_usuario = Column(String, nullable=False) # Guardamos el nombre por si borran al usuario
    accion = Column(String, nullable=False)
    tipo = Column(String, nullable=False) # 'login', 'creacion', 'edicion', etc.
    fecha = Column(DateTime, default=datetime.utcnow)
    ip = Column(String, nullable=True)
    detalles = Column(String, nullable=True)