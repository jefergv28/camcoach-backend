from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class RolUsuario(str, enum.Enum):
    admin = "admin"
    cliente = "cliente"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    rol = Column(SQLEnum(RolUsuario), default=RolUsuario.cliente)
    is_active = Column(Boolean, default=True)

    # 1. Vincular con la tabla Clientes
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)

    # 2. Vincular con el Administrador que lo creó
    admin_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    # --- RELACIONES (DENTRO DE LA CLASE) ---

    # Esta relación debe estar AQUÍ para que reconozca 'cliente_id'
    cliente_perfil = relationship(
        "Cliente",
        back_populates="usuario_cuenta",
        foreign_keys=[cliente_id]
    )

    # Relación para que el administrador vea a quiénes ha creado
    usuarios_creados = relationship(
        "Usuario",
        backref="creado_por",
        remote_side=[id]
    )