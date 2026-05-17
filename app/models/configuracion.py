from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Configuracion(Base):
    __tablename__ = "configuraciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    telefono = Column(String, nullable=True)
    idioma = Column(String, default="es")

    # Canales de notificación
    notif_email = Column(Boolean, default=True)
    notif_whatsapp = Column(Boolean, default=True)
    notif_app = Column(Boolean, default=False)

    # 🎯 LA SOLUCIÓN: Relación unidireccional directa.
    # Quitamos back_populates para evitar que el login dependa del orden de carga de mappers.
    usuario = relationship("Usuario")