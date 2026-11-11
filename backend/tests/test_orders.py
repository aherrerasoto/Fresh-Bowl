
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

        test_client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@freshbowl.cl",
                "password": "FreshBowl123"
            }
        )

        # Crear ingredientes para las pruebas
        test_client.post(
            "/api/v1/ingredients/",
            json={
                "name": "Pollo",
                "category": "Proteinas",
                "price": 1800,
                "stock": 10,
                "available": True
            }
        )

        test_client.post(
            "/api/v1/ingredients/",
            json={
                "name": "Palta",
                "category": "Vegetales",
                "price": 1200,
                "stock": 5,
                "available": True
            }
        )

        yield test_client

    Base.metadata.drop_all(bind=test_engine)


def order_data():
    return {
        "customer_name": "Ana Pérez",
        "customer_email": "ana@example.com",
        "customer_phone": "+56912345678",
        "delivery_method": "retiro",
        "items": [
            {
                "ingredient_id": 1,
                "quantity": 2
            },
            {
                "ingredient_id": 2,
                "quantity": 1
            }
        ]
    }


def create_test_order(client):
    response = client.post(
        "/api/v1/orders/",
        json=order_data()
    )

    return response.json()


def test_create_order(client):
    response = client.post(
        "/api/v1/orders/",
        json=order_data()
    )

    assert response.status_code == 201
    assert response.json()["status"] == "pendiente"
    assert response.json()["total"] == 4800
    assert len(response.json()["items"]) == 2


def test_list_orders(client):
    create_test_order(client)

    response = client.get("/api/v1/orders/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_order(client):
    order = create_test_order(client)

    response = client.get(
        f"/api/v1/orders/{order['id']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == order["id"]


def test_update_order_status(client):
    order = create_test_order(client)

    response = client.patch(
        f"/api/v1/orders/{order['id']}/status",
        json={"status": "confirmado"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "confirmado"


def test_order_with_insufficient_stock(client):
    data = order_data()
    data["items"][0]["quantity"] = 50

    response = client.post(
        "/api/v1/orders/",
        json=data
    )

    assert response.status_code == 409


def test_order_requires_delivery_address(client):
    data = order_data()
    data["delivery_method"] = "despacho"

    response = client.post(
        "/api/v1/orders/",
        json=data
    )

    assert response.status_code == 422


def test_order_rejects_invalid_ingredient(client):
    data = order_data()
    data["items"][0]["ingredient_id"] = 999

    response = client.post(
        "/api/v1/orders/",
        json=data
    )

    assert response.status_code == 404


def test_guest_can_create_order(client):
    client.post("/api/v1/auth/logout")

    response = client.post(
        "/api/v1/orders/",
        json=order_data()
    )

    assert response.status_code == 201


def test_orders_cannot_be_listed_without_login():
    with TestClient(app) as test_client:
        response = test_client.get("/api/v1/orders/")

        assert response.status_code == 401


def test_client_role_cannot_list_orders(client):
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

    response = client.get("/api/v1/orders/")

    assert response.status_code == 403
