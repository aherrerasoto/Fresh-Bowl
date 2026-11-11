from sqlalchemy.orm import Session

from app.orders.models import Order, OrderItem
from app.orders.schemas import OrderCreate, OrderStatusUpdate
from app.inventory.models import Ingredient
from app.clients.models import Client


def get_orders(db: Session):
    return (
        db.query(Order)
        .order_by(Order.id.desc())
        .all()
    )


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def create_order(db: Session, data: OrderCreate):
    # Comprobar que el cliente exista si se indicó uno
    if data.client_id is not None:
        client = (
            db.query(Client)
            .filter(
                Client.id == data.client_id,
                Client.active == True
            )
            .first()
        )

        if not client:
            return "client_not_found"

    # El despacho necesita una dirección
    if data.delivery_method == "despacho" and not data.delivery_address:
        return "address_required"

    # Evitar que un mismo ingrediente aparezca repetido
    ingredient_ids = [item.ingredient_id for item in data.items]

    if len(ingredient_ids) != len(set(ingredient_ids)):
        return "duplicate_items"

    total = 0
    order_items = []

    for item in data.items:
        ingredient = (
            db.query(Ingredient)
            .filter(
                Ingredient.id == item.ingredient_id,
                Ingredient.active == True
            )
            .first()
        )

        if not ingredient:
            return "ingredient_not_found"

        if not ingredient.available:
            return "ingredient_unavailable"

        if ingredient.stock < item.quantity:
            return "insufficient_stock"

        subtotal = ingredient.price * item.quantity
        total += subtotal

        order_items.append(
            OrderItem(
                ingredient_id=ingredient.id,
                ingredient_name=ingredient.name,
                quantity=item.quantity,
                unit_price=ingredient.price,
                subtotal=subtotal
            )
        )

    order = Order(
        client_id=data.client_id,
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        customer_phone=data.customer_phone,
        delivery_method=data.delivery_method,
        delivery_address=data.delivery_address,
        status="pendiente",
        total=total,
        items=order_items
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def update_order_status(
    db: Session,
    order_id: int,
    data: OrderStatusUpdate
):
    order = get_order(db, order_id)

    if not order:
        return None

    order.status = data.status

    db.commit()
    db.refresh(order)

    return order