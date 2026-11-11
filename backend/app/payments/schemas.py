from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PaymentCreate(BaseModel):
    order_id: int = Field(gt=0)
    payment_method: str

    @field_validator("payment_method")
    @classmethod
    def validate_payment_method(cls, value):
        value = value.strip().lower()

        allowed_methods = ["tarjeta", "transferencia"]

        if value not in allowed_methods:
            raise ValueError(
                "El método de pago debe ser tarjeta o transferencia"
            )

        return value


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    amount: int
    payment_method: str
    status: str
    provider_reference: Optional[str]