
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.inventory.models import Ingredient
from app.inventory.schemas import IngredientCreate, IngredientUpdate


def get_ingredients(
    db: Session,
    category=None,
    search=None,
    available=None
):
    query = db.query(Ingredient).filter(Ingredient.active == True)

    if category:
        query = query.filter(Ingredient.category == category)

    if search:
        query = query.filter(
            Ingredient.name.ilike(f"%{search}%")
        )

    if available is not None:
        query = query.filter(Ingredient.available == available)

    return query.order_by(Ingredient.id).all()


def get_ingredient(db: Session, ingredient_id: int):
    return db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.active == True
    ).first()


def create_ingredient(db: Session, data: IngredientCreate):
    existing = db.query(Ingredient).filter(
        func.lower(Ingredient.name) == data.name.lower(),
        Ingredient.active == True
    ).first()

    if existing:
        return None

    ingredient = Ingredient(**data.model_dump())

    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)

    return ingredient


def update_ingredient(
    db: Session,
    ingredient_id: int,
    data: IngredientUpdate
):
    ingredient = get_ingredient(db, ingredient_id)

    if not ingredient:
        return None

    changes = data.model_dump(exclude_unset=True)

    if "name" in changes and changes["name"]:
        duplicate = db.query(Ingredient).filter(
            func.lower(Ingredient.name) == changes["name"].lower(),
            Ingredient.id != ingredient_id,
            Ingredient.active == True
        ).first()

        if duplicate:
            return "duplicate"

    for field, value in changes.items():
        setattr(ingredient, field, value)

    db.commit()
    db.refresh(ingredient)

    return ingredient


def deactivate_ingredient(db: Session, ingredient_id: int):
    ingredient = get_ingredient(db, ingredient_id)

    if not ingredient:
        return False

    ingredient.active = False
    ingredient.available = False

    db.commit()

    return True
