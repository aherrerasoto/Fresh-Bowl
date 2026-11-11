
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.payments import service
from app.payments.schemas import PaymentCreate, PaymentResponse

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.get(
    "/",
    response_model=list[PaymentResponse],
    dependencies=[Depends(require_roles("administrador", "tecnico"))]
)
def list_payments(db: Session = Depends(get_db)):
    return service.get_payments(db)


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
    dependencies=[Depends(require_roles("administrador", "tecnico"))]
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = service.get_payment(db, payment_id)

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Pago no encontrado"
        )

    return payment


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=201
)
def create_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db)
):
    payment = service.create_payment(db, data)

    # Manejo de errores devueltos por el servicio.
    if payment == "payment_exists":
        raise HTTPException(
            status_code=409,
            detail="Este pedido ya tiene un pago registrado"
        )

    if payment == "order_not_found":
        raise HTTPException(
            status_code=404,
            detail="El pedido no existe"
        )

    if payment == "order_cancelled":
        raise HTTPException(
            status_code=409,
            detail="No se puede pagar un pedido cancelado"
    )

    if not payment:
        raise HTTPException(
            status_code=400,
            detail="No se pudo procesar el pago"
        )

    return payment
