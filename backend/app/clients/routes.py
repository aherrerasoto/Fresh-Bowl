from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.clients import service
from app.clients.schemas import (
    ClientCreate,
    ClientUpdate,
    ClientResponse
)

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


@router.get(
    "/",
    response_model=list[ClientResponse],
    dependencies=[Depends(require_roles("administrador"))]
)
def list_clients(db: Session = Depends(get_db)):
    return service.get_clients(db)


@router.get(
    "/{client_id}",
    response_model=ClientResponse,
    dependencies=[Depends(require_roles("administrador"))]
)
def get_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    client = service.get_client(db, client_id)

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    return client


@router.post(
    "/",
    response_model=ClientResponse,
    status_code=201,
    dependencies=[Depends(require_roles("administrador"))]
)
def create_client(
    data: ClientCreate,
    db: Session = Depends(get_db)
):
    client = service.create_client(db, data)

    if client == "duplicate":
        raise HTTPException(
            status_code=409,
            detail="Ya existe un cliente registrado con ese correo"
        )

    return client


@router.patch(
    "/{client_id}",
    response_model=ClientResponse,
    dependencies=[Depends(require_roles("administrador"))]
)
def update_client(
    client_id: int,
    data: ClientUpdate,
    db: Session = Depends(get_db)
):
    client = service.update_client(db, client_id, data)

    if client == "duplicate":
        raise HTTPException(
            status_code=409,
            detail="El correo ya está registrado por otro cliente"
        )

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    return client


@router.delete(
    "/{client_id}",
    dependencies=[Depends(require_roles("administrador"))]
)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    deleted = service.deactivate_client(db, client_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    return {
        "message": "Cliente desactivado correctamente",
        "id": client_id
    }