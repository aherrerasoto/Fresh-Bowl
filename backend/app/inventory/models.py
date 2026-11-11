
from sqlalchemy import Column, Integer, String, Boolean, Text
from app.core.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False, default=0)
    stock = Column(Integer, nullable=False, default=0)
    available = Column(Boolean, nullable=False, default=True)
    active = Column(Boolean, nullable=False, default=True)
