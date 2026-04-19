from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.cliente import Cliente
from app.models.evento import Evento
from app.schemas.reportes import ReporteGeneral, ResumenCliente

# Importamos todos los modelos que necesitamos consultar

from app.models.ingresos import Ingreso

from app.models.tareas import Tarea, EstadoTarea

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

@router.get("/", response_model=ReporteGeneral)
def obtener_reporte_general(db: Session = Depends(get_db)):

    # 1. Obtener todos los clientes
    clientes_db = db.query(Cliente).all()

    resumen_clientes = []
    ingresos_totales = 0.0
    eventos_totales = 0

    # 2. Iterar por cada cliente para calcular sus estadísticas
    for cliente in clientes_db:
        # Sumar ingresos pagados del cliente
        ingresos_cliente = db.query(func.sum(Ingreso.monto))\
            .filter(Ingreso.cliente_id == cliente.id, Ingreso.estado == "pagado").scalar() or 0.0

        # Contar eventos del cliente
        eventos_cliente = db.query(func.count(Evento.id))\
            .filter(Evento.cliente_id == cliente.id).scalar() or 0

        ingresos_totales += ingresos_cliente
        eventos_totales += eventos_cliente

        # Simulación de retención (Por ahora un cálculo estático o aleatorio,
        # luego lo ajustas según tu regla de negocio)
        retencion_simulada = 85 if ingresos_cliente > 0 else 50

        resumen_clientes.append(ResumenCliente(
            id=cliente.id,
            nombre=cliente.nombre,
            ingresos=ingresos_cliente,
            eventos=eventos_cliente,
            retencion=retencion_simulada
        ))

    # 3. Contar todas las tareas completadas globales
    tareas_completadas = db.query(func.count(Tarea.id))\
        .filter(Tarea.estado == EstadoTarea.completado).scalar() or 0

    # 4. Calcular retención promedio global
    retencion_promedio = 0
    if resumen_clientes:
        suma_retencion = sum(c.retencion for c in resumen_clientes)
        retencion_promedio = int(suma_retencion / len(resumen_clientes))

    # 5. Armar y retornar la respuesta final
    return ReporteGeneral(
        ingresos_totales=ingresos_totales,
        eventos_totales=eventos_totales,
        tareas_completadas=tareas_completadas,
        retencion_promedio=retencion_promedio,
        clientes=resumen_clientes
    )