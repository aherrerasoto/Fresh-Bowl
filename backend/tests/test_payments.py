
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
        # Crear administrador de prueba
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
        login_response = test_client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@freshbowl.cl",
                "password": "FreshBowl123"
            }
        )

        assert login_response.status_code == 200

        # Crear ingrediente para los pedidos de prueba
        ingredient_response = test_client.post(
            "/api/v1/ingredients/",
            json={
                "name": "Pollo",
                "category": "Proteinas",
                "price": 1800,
                "stock": 10,
                "available": True
            }
        )

        assert ingredient_response.status_code == 201

        yield test_client

    Base.metadata.drop_all(bind=test_engine)


def create_test_order(client):
    response = client.post(
        "/api/v1/orders/",
        json={
            "customer_name": "Ana Pérez",
            "customer_email": "ana@example.com",
            "customer_phone": "+56912345678",
            "delivery_method": "retiro",
            "items": [
                {
                    "ingredient_id": 1,
                    "quantity": 2
                }
            ]
        }
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_create_payment(client):
    order = create_test_order(client)

    response = client.post(
        "/api/v1/payments/",
        json={
            "order_id": order["id"],
            "payment_method": "tarjeta"
        }
    )

    assert response.status_code == 201
    assert response.json()["status"] == "aprobado"
    assert response.json()["amount"] == 3600
    assert response.json()["provider_reference"] is not None


def test_payment_confirms_order(client):
    order = create_test_order(client)

    client.post(
        "/api/v1/payments/",
        json={
            "order_id": order["id"],
            "payment_method": "tarjeta"
        }
    )

    response = client.get(
        f"/api/v1/orders/{order['id']}"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "confirmado"


def test_duplicate_payment_is_rejected(client):
    order = create_test_order(client)

    payment_data = {
        "order_id": order["id"],
        "payment_method": "tarjeta"
    }

    first_response = client.post(
        "/api/v1/payments/",
        json=payment_data
    )

    second_response = client.post(
        "/api/v1/payments/",
        json=payment_data
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_payment_for_nonexistent_order(client):
    response = client.post(
        "/api/v1/payments/",
        json={
            "order_id": 999,
            "payment_method": "tarjeta"
        }
    )

    assert response.status_code == 404


def test_payment_for_cancelled_order(client):
    order = create_test_order(client)

    cancel_response = client.patch(
        f"/api/v1/orders/{order['id']}/status",
        json={"status": "cancelado"}
    )

    assert cancel_response.status_code == 200

    response = client.post(
        "/api/v1/payments/",
        json={
            "order_id": order["id"],
            "payment_method": "tarjeta"
        }
    )

    assert response.status_code == 409


def test_invalid_payment_method(client):
    order = create_test_order(client)

    response = client.post(
        "/api/v1/payments/",
        json={
            "order_id": order["id"],
            "payment_method": "bitcoin"
        }
    )

    assert response.status_code == 422


def test_list_payments(client):
    order = create_test_order(client)

    client.post(
        "/api/v1/payments/",
        json={
            "order_id": order["id"],
            "payment_method": "transferencia"
        }
    )

    response = client.get("/api/v1/payments/")

    assert response.status_code == 200
    assert len(response.json()) == 1
