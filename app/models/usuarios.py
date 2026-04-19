from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
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
    hashed_password = Column(String, nullable=False) # Las contraseñas siempre van encriptadas
    rol = Column(SQLEnum(RolUsuario), default=RolUsuario.cliente)
    is_active = Column(Boolean, default=True)

    # Si el rol es 'cliente', este campo lo enlaza con su perfil en la tabla Clientes
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)