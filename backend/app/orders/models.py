from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=True
    )

    # Datos de contacto para compras de invitados
    customer_name = Column(String(120), nullable=False)
    customer_email = Column(String(150), nullable=False)
    customer_phone = Column(String(20), nullable=False)

    delivery_method = Column(String(20), nullable=False)
    delivery_address = Column(Text, nullable=True)

    status = Column(String(30), nullable=False, default="pendiente")

    total = Column(Integer, nullable=False, default=0)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    ingredient_id = Column(
        Integer,
        ForeignKey("ingredients.id"),
        nullable=False
    )

    ingredient_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")