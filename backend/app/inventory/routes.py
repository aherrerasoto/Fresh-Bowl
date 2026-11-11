from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.inventory import service
from app.inventory.schemas import (
    IngredientCreate,
    IngredientUpdate,
    IngredientResponse
)

router = APIRouter(
    prefix="/ingredients",
    tags=["Inventory"]
)


@router.get("/", response_model=list[IngredientResponse])
def list_ingredients(
    category: str | None = None,
    search: str | None = None,
    available: bool | None = None,
    db: Session = Depends(get_db)
):
    return service.get_ingredients(
        db,
        category,
        search,
        available
    )


@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db)
):
    ingredient = service.get_ingredient(db, ingredient_id)

    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente no encontrado"
        )

    return ingredient


@router.post(
    "/",
    response_model=IngredientResponse,
    status_code=201,
    dependencies=[Depends(require_roles("administrador"))]
)
def create_ingredient(
    data: IngredientCreate,
    db: Session = Depends(get_db)
):
    ingredient = service.create_ingredient(db, data)

    if ingredient is None:
        raise HTTPException(
            status_code=409,
            detail="El ingrediente ya existe"
        )

    return ingredient


@router.patch(
    "/{ingredient_id}",
    response_model=IngredientResponse,
    dependencies=[Depends(require_roles("administrador"))]
)
def update_ingredient(
    ingredient_id: int,
    data: IngredientUpdate,
    db: Session = Depends(get_db)
):
    ingredient = service.update_ingredient(
        db,
        ingredient_id,
        data
    )

    if ingredient == "duplicate":
        raise HTTPException(
            status_code=409,
            detail="El nombre ya está registrado"
        )

    if ingredient is None:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente no encontrado"
        )

    return ingredient


@router.delete(
    "/{ingredient_id}",
    dependencies=[Depends(require_roles("administrador"))]
)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db)
):
    deleted = service.deactivate_ingredient(db, ingredient_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente no encontrado"
        )

    return {
        "message": "Ingrediente desactivado correctamente",
        "id": ingredient_id
    }