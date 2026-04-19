from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def create_usuario(db: Session, usuario: UsuarioCreate):
    # IMPORTANTE: Aquí se debe encriptar la contraseña antes de guardarla.
    # Ejemplo: hashed_pwd = get_password_hash(usuario.password)
    fake_hashed_password = usuario.password + "notreallyhashed"

    db_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        hashed_password=fake_hashed_password,
        rol=usuario.rol,
        cliente_id=usuario.cliente_id
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario:
        update_data = usuario_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario