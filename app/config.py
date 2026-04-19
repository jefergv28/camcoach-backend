from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Carga .env

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    OPENAI_API_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int   # Sin valor default, lo toma de .env


class Config:
    env_file = ".env"
    extra = "allow"

settings = Settings()