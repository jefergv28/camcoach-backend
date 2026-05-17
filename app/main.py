from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

from app.routers import (
    auth,
    buscador,
    clientes,
    configuracion,
    eventos,
    ingresos,
    tareas,
    capacitaciones,
    reportes,
    usuarios,
)

# 🔥 IMPORTANTE: no cargar dotenv aquí si ya lo haces en config
# load_dotenv() -> opcional si lo usas en settings

app = FastAPI(
    title="CamCoach Backend",
    description="API para gestión de creadores de contenido",
    version="1.0.0"
)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
)

# =========================
# ROUTERS
# =========================
app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(eventos.router)
app.include_router(ingresos.router)
app.include_router(tareas.router)
app.include_router(capacitaciones.router)
app.include_router(reportes.router)
app.include_router(usuarios.router)
app.include_router(configuracion.router)
app.include_router(buscador.router)

# =========================
# STARTUP (CLAVE)
# =========================
@app.on_event("startup")
def on_startup():
    """
    Crea las tablas en la base de datos cuando arranca el servidor.
    Evita errores de importación temprana.
    """
    Base.metadata.create_all(bind=engine)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "message": "CamCoach Backend - Listo y funcionando 🚀"
    }