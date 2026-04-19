from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from app.crud.cliente import create_cliente, get_cliente, get_clientes, update_cliente, delete_cliente
from app.utils.auth import get_current_user
from app.schemas.auth import TokenData

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteOut, status_code=status.HTTP_201_CREATED)
def create_new_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user)  # Solo admin crea
):
    return create_cliente(db, cliente)

@router.get("/", response_model=List[ClienteOut])
def read_clientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)  # Logueados ven
):
    return get_clientes(db, skip=skip, limit=limit)

@router.get("/{cliente_id}", response_model=ClienteOut)
def read_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.put("/{cliente_id}", response_model=ClienteOut)
def update_existing_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user)
):
    db_cliente = update_cliente(db, cliente_id, cliente_update)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.delete("/{cliente_id}", response_model=ClienteOut)
def delete_existing_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user)
):
    db_cliente = delete_cliente(db, cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente