from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum as SQLEnum
from datetime import datetime
from app.database import Base
import enum
from sqlalchemy.orm import relationship

class EstadoCliente(str, enum.Enum):
    activa = "activa"
    pausada = "pausada"

class Cliente(Base):
    __tablename__ = "clientes"

    # 1. COLUMNAS (Definirlas primero)
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True) # ID del Admin dueño
    nombre = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=True)
    whatsapp = Column(String, nullable=True)
    plataforma_principal = Column(String, nullable=False)
    estado = Column(SQLEnum(EstadoCliente), default=EstadoCliente.activa)
    ingresos_mes = Column(Float, default=0.0)
    fecha_union = Column(DateTime, default=datetime.utcnow)

    # 2. RELACIONES (Dentro de la clase y después de las columnas)

    # Enlace con la cuenta de usuario del cliente
    usuario_cuenta = relationship(
        "Usuario",
        back_populates="cliente_perfil",
        uselist=False,
        foreign_keys="[Usuario.cliente_id]"
    )

    # Enlace con el Administrador que lo creó
    admin_creador = relationship(
        "Usuario",
        foreign_keys=[admin_id]
    )

    def __repr__(self):
        return f"<Cliente {self.nombre} - {self.estado}>"