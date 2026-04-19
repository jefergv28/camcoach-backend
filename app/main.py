from fastapi import FastAPI
from app.database import engine, Base  # Importamos Base que contiene todas las tablas
from app.routers import auth, clientes, eventos
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routers import ingresos
from app.routers import tareas
from app.routers import capacitaciones
from app.routers import reportes

load_dotenv()  # Carga variables del archivo .env
# Esto crea TODAS las tablas definidas en app.models (User, Evento, Cliente, etc.)
# Siempre y cuando tus modelos hereden de Base
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CamCoach Backend",
    description="API para gestión de creadores de contenido",
    version="1.0.0"
)

# Configuración de CORS corregida para producción y cookies
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"], # Simplificado para aceptar todos los métodos
    allow_headers=["*"], # Simplificado para aceptar todos los headers
    expose_headers=["set-cookie"],
)

# Incluye los routers una sola vez
app.include_router(auth.router)
app.include_router(eventos.router)
app.include_router(clientes.router)
app.include_router(ingresos.router)
app.include_router(tareas.router)
app.include_router(capacitaciones.router)
app.include_router(reportes.router)

@app.get("/")
def root():
    return {"message": "CamCoach Backend - Listo y funcionando"}