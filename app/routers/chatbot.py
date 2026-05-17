import os
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.auth import get_current_user
from app.models.usuarios import Usuario

import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🔑 IMPORTAMOS LOS MODELOS PARA DARLE CONTEXTO PRIVADO A LA IA
from app.models.cliente import Cliente

# Nota: Si tu modelo de tareas en app/models/ se llama diferente, ajusta la importación
# from app.models.tareas import Tarea

router = APIRouter(prefix="/chat", tags=["Chatbot Inteligente"])


class ChatRequest(BaseModel):
    mensaje: str


# 🔐 PROTECCIÓN DE LLAVE: Busca primero en las variables de entorno (.env)
# Si no existe, usa la tuya como Plan B temporal (¡pero lo ideal es sacarla de aquí!)


@router.post("/")
async def chat_inteligente(
    payload: ChatRequest,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 🛡️ VALIDACIÓN DE LA LLAVE
    if not GROQ_API_KEY or GROQ_API_KEY == "TU_LLAVE_GSK_AQUI":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falta la API Key de Groq en el configuración del servidor.",
        )

    # 📊 EXTRACTO DE CONTEXTO PRIVADO
    # Contamos los clientes reales que le pertenecen ÚNICAMENTE a este administrador
    total_clientes_propios = (
        db.query(Cliente).filter(Cliente.admin_id == current_user.id).count()
    )

    # 🤖 1. DEFINICIÓN DE ROLES CON MENSAJE DEL SISTEMA REAL
    if current_user.rol == "admin":
        system_instruction = (
            f"Eres el Asistente Administrativo y Analista de Negocios de CamCoach. "
            f"Estás hablando con el Administrador de la plataforma: {current_user.username}. "
            f"Actualmente este administrador gestiona un total de {total_clientes_propios} clientes en su base de datos. "
            "Tu objetivo es ayudarlo a analizar métricas, dar consejos de gestión de finanzas, "
            "retención de clientes y optimización de asesorías basados únicamente en sus datos. "
            "Sé profesional, directo y ejecutivo."
        )
    else:
        system_instruction = (
            f"Eres el Co-Coach Deportivo virtual de CamCoach. "
            f"Estás hablando con el Cliente: {current_user.username}. "
            "Tu objetivo es guiarlo en sus entrenamientos, resolver dudas de rutinas, explicar "
            "técnicas de ejercicios, dar consejos de nutrición y mantenerlo motivado en su plan. "
            "Sé empático, entusiasta, claro y usa emojis deportivos."
        )

    # 🔗 2. ENDPOINT ESTÁNDAR DE OPENAI/GROQ
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": payload.mensaje},
        ],
        "temperature": 0.7,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=body, headers=headers, timeout=20.0)

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error del proveedor de IA (Groq): {response.text}",
            )

        data = response.json()
        respuesta_ia = data["choices"][0]["message"]["content"]

        return {"respuesta": respuesta_ia}

    except HTTPException as he:
        raise he
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No se pudo conectar con Groq: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno en el módulo de chat: {str(e)}",
        )
