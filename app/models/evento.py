import sqlalchemy
from sqlalchemy import Column, ForeignKey # 👈 IMPORTACIONES NECESARIAS
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    titulo = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    fecha = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # Guardamos como string ISO para match con el front
    hora = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cliente = sqlalchemy.Column(sqlalchemy.String, nullable=False) # Nombre del cliente (como lo tienes en el front)
    descripcion = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    miRecordatorio = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    notificarCliente = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    tipoNotifCliente = sqlalchemy.Column(sqlalchemy.String, nullable=True) # "whatsapp" | "email" | "sms"

    # 🎯 EL CANDADO DEFINITIVO: Conexión física con el administrador dueño del evento
    # (Asegúrate de que el __tablename__ de tu modelo de usuarios sea exactamente "usuarios")
    usuario_id = Column(sqlalchemy.Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"<Evento {self.titulo} - {self.cliente}>"