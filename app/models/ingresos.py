from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
import datetime
from app.database import Base
class Ingreso(Base):
    __tablename__ = "ingresos"

    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Float, nullable=False)
    fecha = Column(Date, default=datetime.date.today)
    descripcion = Column(String, nullable=True)
    metodo_pago = Column(String, default="efectivo") # efectivo, transferencia, tarjeta
    estado = Column(String, default="pagado") # pagado, pendiente

    # Llave foránea conectando al cliente
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    # Relación (Opcional, si tienes el modelo Cliente definido)
    # cliente = relationship("Cliente", back_populates="ingresos")