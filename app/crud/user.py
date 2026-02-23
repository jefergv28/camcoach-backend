from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserCreate

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    # Rol forzado: solo "cliente" al registrarse
    hashed_password = User.hash_password(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        rol="cliente"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user