from fastapi import FastAPI
from app.database import engine
from app.models.user import User  # Importa para crear tablas
from app.routers import auth
from fastapi.middleware.cors import CORSMiddleware


# Crea tablas automáticamente (solo para desarrollo)
User.metadata.create_all(bind=engine)

app = FastAPI(
    title="CamCoach Backend",
    description="API para gestión de creadores de contenido",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    expose_headers=["set-cookie"],  # ← Agrega esto para que el navegador vea set-cookie
)

# Incluye routers
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "CamCoach Backend - Listo para autenticación"}