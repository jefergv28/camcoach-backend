# app/utils/security.py
from passlib.context import CryptContext

# Forzamos bcrypt explícitamente
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_hash_password(password: str) -> str:
    hash_result = pwd_context.hash(password)
    # CHISMOSO: Imprimimos el hash que se genera para ver si se ve completo
    print(f"🔐 HASH GENERADO para '{password}': {hash_result}")
    return hash_result

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    # CHISMOSO: Imprimimos qué está comparando
    print(f"🔍 VERIFICANDO: Clave plana '{plain_password}' contra Hash guardado: '{hashed_password}'")

    es_valido = pwd_context.verify(plain_password, hashed_password)
    print(f"📊 RESULTADO VERIFICACIÓN: {es_valido}")

    return es_valido