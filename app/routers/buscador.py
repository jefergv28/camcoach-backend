from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from app.database import get_db
from app.models.cliente import Cliente
from app.models.ingresos import Ingreso
from app.models.usuarios import Usuario


# 🔑 DESCOMENTAMOS LOS MODELOS PARA INTEGRARLOS DE FORMA SEGURA
from app.models.evento import Evento

from app.utils.auth import get_current_user

router = APIRouter(prefix="/buscador", tags=["Buscador Inteligente"])


# ----------------------------------------------------------------
# ENDPOINT 1: BÚSQUEDA GLOBAL MULTI-MÓDULO (BLINDADO)
# ----------------------------------------------------------------
@router.get("/")
def buscar_global(
    q: str = Query("", description="Texto a buscar"),
    tipo: str = Query("todo", description="Filtro manual"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    resultados = []
    texto_busqueda = q.lower().strip()
    query_text = f"%{texto_busqueda}%"

    # 🤖 MINI-MOTOR DE INTENCIÓN (IA HEURÍSTICA)
    filtrar_estado = None
    if "activ" in texto_busqueda:
        filtrar_estado = "activa"
    elif "pausad" in texto_busqueda:
        filtrar_estado = "pausada"

    palabras_limpias = [
        p
        for p in texto_busqueda.split()
        if p not in ["clientes", "activos", "activas", "pausados", "pausadas", "ver", "eventos", "ingresos"]
    ]
    busqueda_limpia = (
        f"%{' '.join(palabras_limpias)}%" if palabras_limpias else query_text
    )

    # ==========================================
    # A. BUSCAR EN CLIENTES (Tu código base seguro)
    # ==========================================
    if tipo in ["todo", "clientes"] and texto_busqueda:
        query_base_clientes = db.query(Cliente).filter(Cliente.admin_id == current_user.id)

        if filtrar_estado:
            if palabras_limpias:
                clientes = query_base_clientes.filter(
                    Cliente.nombre.ilike(busqueda_limpia),
                    Cliente.estado == filtrar_estado,
                ).all()
            else:
                clientes = query_base_clientes.filter(Cliente.estado == filtrar_estado).all()
        else:
            clientes = query_base_clientes.filter(
                (Cliente.nombre.ilike(query_text)) | (Cliente.email.ilike(query_text))
            ).all()

        for c in clientes:
            resultados.append({
                "id": f"cli-{c.id}",
                "modulo": "clientes",
                "titulo": c.nombre,
                "subtitulo": f"✉️ {c.email}",
                "badge": c.estado,
                "monto": c.ingresos_mes,
                "fecha": c.fecha_union.strftime("%Y-%m-%d") if c.fecha_union else None,
                "detalles": f"📱 Tel: {c.telefono or 'No registra'}",
            })

    # ==========================================
    # B. BUSCAR EN EVENTOS (Añadido con Candado Segurísimo)
    # ==========================================
    if tipo in ["todo", "eventos"] and texto_busqueda:
        # 🎯 FILTRO CLAVE: Solo busca eventos cuyo usuario_id (o admin_id) sea el del logueado
        # Ajusta 'usuario_id' según cómo se llame la columna FK en tu modelo Evento
        eventos = db.query(Evento).filter(
            Evento.usuario_id == current_user.id,
            Evento.titulo.ilike(query_text)
        ).all()

        for e in eventos:
            resultados.append({
                "id": f"eve-{e.id}",
                "modulo": "eventos",
                "titulo": e.titulo,
                "subtitulo": "📅 Agenda / Evento",
                "badge": e.estado if hasattr(e, 'estado') else "Programado",
                "monto": 0,
                "fecha": e.fecha.strftime("%Y-%m-%d") if e.fecha else None,
                "detalles": e.descripcion or "Sin descripción adicional",
            })

    # ==========================================
    # C. BUSCAR EN INGRESOS (Añadido con Candado Segurísimo)
    # ==========================================
    if tipo in ["todo", "ingresos"] and texto_busqueda:
        # 🎯 FILTRO CLAVE: Solo busca ingresos que pertenezcan a este administrador
        # Ajusta 'usuario_id' según cómo se llame la columna FK en tu modelo Ingreso
        ingresos = db.query(Ingreso).filter(
            Ingreso.usuario_id == current_user.id,
            Ingreso.descripcion.ilike(query_text)
        ).all()

        for i in ingresos:
            resultados.append({
                "id": f"ing-{i.id}",
                "modulo": "ingresos",
                "titulo": i.descripcion or "Ingreso registrado",
                "subtitulo": "💵 Flujo de caja",
                "badge": "Pago Exitoso",
                "monto": i.monto,
                "fecha": i.fecha.strftime("%Y-%m-%d") if i.fecha else None,
                "detalles": f"Monto completo recibido de asesoría",
            })

    return resultados


# ----------------------------------------------------------------
# ENDPOINT 2: MOTOR DE RECOMENDACIONES "IA" (Sigue protegido)
# ----------------------------------------------------------------
@router.get("/recomendaciones")
def obtener_sugerencias_ia(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    sugerencias = []

    # Heurística 1: Clientes pausados del ADMIN actual
    clientes_pausados = (
        db.query(Cliente)
        .filter(Cliente.admin_id == current_user.id, Cliente.estado == "pausada")
        .count()
    )

    if clientes_pausados > 0:
        sugerencias.append(f"Contactar {clientes_pausados} clientes pausados")

    # Heurística 2: Salud financiera del ADMIN actual
    clientes_bajos_ingresos = (
        db.query(Cliente)
        .filter(Cliente.admin_id == current_user.id, Cliente.ingresos_mes < 200000)
        .count()
    )

    if clientes_bajos_ingresos > 0:
        sugerencias.append("Revisar tarifas de asesorías")

    if not sugerencias:
        sugerencias = [
            "Programar nuevas asesorías",
            "Ver balance de ingresos del mes",
            "Auditar bitácora de clientes nuevos",
        ]

    return sugerencias[:3]