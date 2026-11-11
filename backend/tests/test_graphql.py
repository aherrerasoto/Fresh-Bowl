
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

        login_response = test_client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@freshbowl.cl",
                "password": "FreshBowl123"
            }
        )

        assert login_response.status_code == 200

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

        yield test_client

    Base.metadata.drop_all(bind=test_engine)


def test_graphql_ingredients(client):
    response = client.post(
        "/api/v1/graphql",
        json={
            "query": """
                query {
                    ingredients {
                        id
                        name
                        category
                        price
                        stock
                    }
                }
            """
        }
    )

    assert response.status_code == 200
    assert "errors" not in response.json()
    assert response.json()["data"]["ingredients"][0]["name"] == "Pollo"


def test_graphql_orders(client):
    response = client.post(
        "/api/v1/graphql",
        json={
            "query": """
                query {
                    orders {
                        id
                        customerName
                        status
                        deliveryMethod
                        total
                    }
                }
            """
        }
    )

    assert response.status_code == 200
    assert "errors" not in response.json()
    assert len(response.json()["data"]["orders"]) == 1


def test_graphql_dashboard(client):
    response = client.post(
        "/api/v1/graphql",
        json={
            "query": """
                query {
                    dashboard {
                        availableIngredients
                        totalOrders
                        totalSales
                    }
                }
            """
        }
    )

    assert response.status_code == 200
    assert "errors" not in response.json()

    dashboard = response.json()["data"]["dashboard"]

    assert dashboard["availableIngredients"] == 1
    assert dashboard["totalOrders"] == 1
    assert dashboard["totalSales"] == 3600


def test_graphql_requires_authentication():
    with TestClient(app) as test_client:
        response = test_client.post(
            "/api/v1/graphql",
            json={
                "query": """
                    query {
                        ingredients {
                            id
                            name
                        }
                    }
                """
            }
        )

        assert response.status_code == 401
