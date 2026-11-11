
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.auth.models import User
from app.core.security import hash_password


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    with TestClient(app) as test_client:
        db = TestingSessionLocal()

        admin = User(
            full_name="Administrador de prueba",
            email="admin@freshbowl.cl",
            password_hash=hash_password("FreshBowl123"),
            role="administrador",
            active=True
        )

        db.add(admin)
        db.commit()
        db.close()

        # Iniciar sesión como administrador
        test_client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@freshbowl.cl",
                "password": "FreshBowl123"
            }
        )

        yield test_client

    Base.metadata.drop_all(bind=test_engine)


def test_create_ingredient(client):
    response = client.post(
        "/api/v1/ingredients/",
        json={
            "name": "Pollo",
            "category": "Proteinas",
            "description": "Pollo a la plancha",
            "price": 1800,
            "stock": 20,
            "available": True
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Pollo"


def test_list_ingredients(client):
    client.post(
        "/api/v1/ingredients/",
        json={
            "name": "Palta",
            "category": "Vegetales",
            "price": 1200,
            "stock": 10
        }
    )

    response = client.get("/api/v1/ingredients/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_ingredient(client):
    created = client.post(
        "/api/v1/ingredients/",
        json={
            "name": "Quinoa",
            "category": "Extras",
            "price": 900,
            "stock": 15
        }
    )

    ingredient_id = created.json()["id"]

    response = client.get(
        f"/api/v1/ingredients/{ingredient_id}"
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Quinoa"


def test_update_ingredient(client):
    created = client.post(
        "/api/v1/ingredients/",
        json={
            "name": "Tomate",
            "category": "Vegetales",
            "price": 500,
            "stock": 10
        }
    )

    ingredient_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/ingredients/{ingredient_id}",
        json={"price": 700}
    )

    assert response.status_code == 200
    assert response.json()["price"] == 700


def test_deactivate_ingredient(client):
    created = client.post(
        "/api/v1/ingredients/",
        json={
            "name": "Aderezo",
            "category": "Salsas",
            "price": 400,
            "stock": 5
        }
    )

    ingredient_id = created.json()["id"]

    response = client.delete(
        f"/api/v1/ingredients/{ingredient_id}"
    )

    assert response.status_code == 200

    detail = client.get(
        f"/api/v1/ingredients/{ingredient_id}"
    )

    assert detail.status_code == 404


def test_duplicate_ingredient(client):
    ingredient = {
        "name": "Pollo",
        "category": "Proteinas",
        "price": 1800,
        "stock": 20
    }

    client.post("/api/v1/ingredients/", json=ingredient)

    response = client.post(
        "/api/v1/ingredients/",
        json=ingredient
    )

    assert response.status_code == 409


def test_negative_price_is_rejected(client):
    response = client.post(
        "/api/v1/ingredients/",
        json={
            "name": "Ingrediente inválido",
            "category": "Extras",
            "price": -100,
            "stock": 5
        }
    )

    assert response.status_code == 422


def test_create_ingredient_without_login():
    with TestClient(app) as test_client:
        response = test_client.post(
            "/api/v1/ingredients/",
            json={
                "name": "Zanahoria",
                "category": "Vegetales",
                "price": 500,
                "stock": 10
            }
        )

        assert response.status_code == 401


def test_client_role_cannot_create_ingredient(client):
    client.post("/api/v1/auth/logout")

    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Cliente de prueba",
            "email": "cliente@freshbowl.cl",
            "password": "Cliente123"
        }
    )

    client.post(
        "/api/v1/auth/login",
        json={
            "email": "cliente@freshbowl.cl",
            "password": "Cliente123"
        }
    )

    response = client.post(
        "/api/v1/ingredients/",
        json={
            "name": "Zanahoria",
            "category": "Vegetales",
            "price": 500,
            "stock": 10
        }
    )

    assert response.status_code == 403
