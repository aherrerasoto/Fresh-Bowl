from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrderItemCreate(BaseModel):
    ingredient_id: int = Field(gt=0)
    quantity: int = Field(ge=1)


class OrderCreate(BaseModel):
    client_id: Optional[int] = Field(default=None, gt=0)

    customer_name: str = Field(min_length=2, max_length=120)
    customer_email: str = Field(min_length=5, max_length=150)
    customer_phone: str = Field(min_length=8, max_length=20)

    delivery_method: str
    delivery_address: Optional[str] = None

    items: list[OrderItemCreate] = Field(min_length=1)

    @field_validator("customer_name")
    @classmethod
    def validate_name(cls, value):
        return value.strip()

    @field_validator("customer_email")
    @classmethod
    def validate_email(cls, value):
        value = value.strip().lower()
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Correo electrónico no válido")
        return value

    @field_validator("customer_phone")
    @classmethod
    def validate_phone(cls, value):
        value = value.strip()
        if not all(char in "0123456789+()- " for char in value):
            raise ValueError("Teléfono no válido")
        return value

    @field_validator("delivery_method")
    @classmethod
    def validate_delivery_method(cls, value):
        value = value.strip().lower()
        if value not in ["retiro", "despacho"]:
            raise ValueError("La modalidad debe ser retiro o despacho")
        return value

    @field_validator("delivery_address")
    @classmethod
    def validate_address(cls, value):
        if value is not None:
            value = value.strip() or None
        return value


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ingredient_id: int
    ingredient_name: str
    quantity: int
    unit_price: int
    subtotal: int


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: Optional[int]
    customer_name: str
    customer_email: str
    customer_phone: str
    delivery_method: str
    delivery_address: Optional[str]
    status: str
    total: int
    items: list[OrderItemResponse]


class OrderStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        value = value.strip().lower()

        allowed_statuses = [
            "pendiente",
            "confirmado",
            "en_preparacion",
            "listo",
            "en_camino",
            "entregado",
            "cancelado"
        ]

        if value not in allowed_statuses:
            raise ValueError("Estado de pedido no válido")

        return value