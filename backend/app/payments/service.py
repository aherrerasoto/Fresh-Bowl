from uuid import uuid4

from sqlalchemy.orm import Session

from app.payments.models import Payment
from app.payments.schemas import PaymentCreate
from app.orders.models import Order


def simulate_payment_provider(amount: int, payment_method: str):
    """
    Simula la respuesta de un proveedor externo de pagos.
    No realiza transacciones bancarias reales.
    """

    if amount <= 0:
        return {
            "approved": False,
            "reference": None
        }

    return {
        "approved": True,
        "reference": f"FB-{uuid4().hex[:12].upper()}"
    }


def get_payments(db: Session):
    return db.query(Payment).order_by(Payment.id.desc()).all()


def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()


def create_payment(db: Session, data: PaymentCreate):
    order = (
        db.query(Order)
        .filter(Order.id == data.order_id)
        .first()
    )

    if not order:
        return "order_not_found"

    if order.status == "cancelado":
        return "order_cancelled"

    existing_payment = (
        db.query(Payment)
        .filter(Payment.order_id == data.order_id)
        .first()
    )

    if existing_payment:
        return "payment_exists"

    # El monto se obtiene del pedido almacenado en el backend.
    payment_result = simulate_payment_provider(
        order.total,
        data.payment_method
    )

    if payment_result["approved"]:
        payment_status = "aprobado"
        order.status = "confirmado"
    else:
        payment_status = "rechazado"

    payment = Payment(
        order_id=order.id,
        amount=order.total,
        payment_method=data.payment_method,
        status=payment_status,
        provider_reference=payment_result["reference"]
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment