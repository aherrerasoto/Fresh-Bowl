
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class IngredientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2, max_length=50)
    description: Optional[str] = None
    price: int = Field(ge=0)
    stock: int = Field(default=0, ge=0)
    available: bool = True


class IngredientUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    category: Optional[str] = Field(default=None, min_length=2, max_length=50)
    description: Optional[str] = None
    price: Optional[int] = Field(default=None, ge=0)
    stock: Optional[int] = Field(default=None, ge=0)
    available: Optional[bool] = None


class IngredientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    description: Optional[str]
    price: int
    stock: int
    available: bool
    active: bool
