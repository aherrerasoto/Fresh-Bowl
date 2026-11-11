from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles

from app.orders import service
from app.orders.schemas import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.get(
    "/",
    response_model=list[OrderResponse],
    dependencies=[Depends(require_roles("administrador", "tecnico"))]
)
def list_orders(db: Session = Depends(get_db)):
    return service.get_orders(db)


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    dependencies=[Depends(require_roles("administrador", "tecnico"))]
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = service.get_order(db, order_id)

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    return order


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=201
)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db)
):
    order = service.create_order(db, data)

    errors = {
        "client_not_found": (404, "Cliente no encontrado"),
        "address_required": (
            422,
            "Debe ingresar una dirección para el despacho"
        ),
        "duplicate_items": (
            422,
            "No repita ingredientes en el pedido"
        ),
        "ingredient_not_found": (
            404,
            "Uno de los ingredientes no existe"
        ),
        "ingredient_unavailable": (
            409,
            "Uno de los ingredientes no está disponible"
        ),
        "insufficient_stock": (
            409,
            "No hay stock suficiente de uno de los ingredientes"
        )
    }

    if isinstance(order, str) and order in errors:
        status_code, message = errors[order]

        raise HTTPException(
            status_code=status_code,
            detail=message
        )

    return order


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
    dependencies=[Depends(require_roles("administrador", "tecnico"))]
)
def change_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    order = service.update_order_status(db, order_id, data)

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    return order