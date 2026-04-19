from pydantic import BaseModel
from typing import List

class ResumenCliente(BaseModel):
    id: int
    nombre: str
    ingresos: float
    eventos: int
    retencion: int # Opcional: Esto lo podemos calcular o simular

class ReporteGeneral(BaseModel):
    ingresos_totales: float
    eventos_totales: int
    tareas_completadas: int
    retencion_promedio: int
    clientes: List[ResumenCliente]