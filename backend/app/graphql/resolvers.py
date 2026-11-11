from sqlalchemy.orm import Session
from sqlalchemy import func

from app.inventory.models import Ingredient
from app.orders.models import Order


def get_ingredients_data(db: Session):
    ingredients = (
        db.query(Ingredient)
        .filter(
            Ingredient.active == True,
            Ingredient.available == True
        )
        .order_by(Ingredient.id)
        .all()
    )

    return [
        {
            "id": ingredient.id,
            "name": ingredient.name,
            "category": ingredient.category,
            "price": ingredient.price,
            "stock": ingredient.stock
        }
        for ingredient in ingredients
    ]


def get_orders_data(db: Session):
    orders = (
        db.query(Order)
        .order_by(Order.id.desc())
        .all()
    )

    return [
        {
            "id": order.id,
            "customer_name": order.customer_name,
            "status": order.status,
            "delivery_method": order.delivery_method,
            "total": order.total
        }
        for order in orders
    ]


def get_dashboard_data(db: Session):
    available_ingredients = (
        db.query(Ingredient)
        .filter(
            Ingredient.active == True,
            Ingredient.available == True
        )
        .count()
    )

    total_orders = db.query(Order).count()

    total_sales = (
        db.query(func.sum(Order.total))
        .filter(Order.status != "cancelado")
        .scalar()
    )

    return {
        "available_ingredients": available_ingredients,
        "total_orders": total_orders,
        "total_sales": total_sales or 0
    }