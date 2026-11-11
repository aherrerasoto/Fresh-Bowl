import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ClientCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=20)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):
        value = value.strip()
        if len(value) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        value = value.strip().lower()
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, value):
            raise ValueError("Debe ingresar un correo electrónico válido")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None:
            value = value.strip()
            if value and not re.match(r"^[0-9+()\-\s]{8,20}$", value):
                raise ValueError("El teléfono contiene caracteres no válidos")
            return value or None
        return value


class ClientUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    email: Optional[str] = Field(default=None, min_length=5, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=20)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):
        if value is not None:
            value = value.strip()
            if len(value) < 2:
                raise ValueError("El nombre debe tener al menos 2 caracteres")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if value is not None:
            value = value.strip().lower()
            pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
            if not re.match(pattern, value):
                raise ValueError("Debe ingresar un correo electrónico válido")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None:
            value = value.strip()
            if value and not re.match(r"^[0-9+()\-\s]{8,20}$", value):
                raise ValueError("El teléfono contiene caracteres no válidos")
            return value or None
        return value


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    phone: Optional[str]
    active: bool