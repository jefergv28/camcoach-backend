from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

def create_cliente(db: Session, cliente: ClienteCreate, admin_id: int):
    # Forzamos que se guarde con el ID del administrador dueño
    db_cliente = Cliente(**cliente.dict(), admin_id=admin_id)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def get_clientes(db: Session, admin_id: int, skip: int = 0, limit: int = 100):
    # 🔑 AQUÍ SE HACE MAGIA: Filtramos directo en la consulta de base de datos
    return db.query(Cliente).filter(Cliente.admin_id == admin_id).offset(skip).limit(limit).all()

def get_cliente(db: Session, cliente_id: int, admin_id: int):
    # Evita que un Admin vea el cliente de otro adivinando el ID en la URL
    return db.query(Cliente).filter(Cliente.id == cliente_id, Cliente.admin_id == admin_id).first()

def update_cliente(db: Session, cliente_id: int, cliente_update: ClienteUpdate, admin_id: int):
    db_cliente = get_cliente(db, cliente_id, admin_id=admin_id)
    if not db_cliente:
        return None
    for key, value in cliente_update.dict(exclude_unset=True).items():
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, cliente_id: int, admin_id: int):
    db_cliente = get_cliente(db, cliente_id, admin_id=admin_id)
    if not db_cliente:
        return None
    db.delete(db_cliente)
    db.commit()
    return db_cliente