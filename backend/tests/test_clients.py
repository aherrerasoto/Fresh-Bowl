
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

        yield test_client

    Base.metadata.drop_all(bind=test_engine)


def test_create_client(client):
    response = client.post(
        "/api/v1/clients/",
        json={
            "full_name": "Ana Pérez",
            "email": "ana@example.com",
            "phone": "+56912345678"
        }
    )

    assert response.status_code == 201
    assert response.json()["full_name"] == "Ana Pérez"
    assert response.json()["email"] == "ana@example.com"


def test_list_clients(client):
    client.post(
        "/api/v1/clients/",
        json={
            "full_name": "Ana Pérez",
            "email": "ana@example.com"
        }
    )

    response = client.get("/api/v1/clients/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_client(client):
    created = client.post(
        "/api/v1/clients/",
        json={
            "full_name": "Ana Pérez",
            "email": "ana@example.com"
        }
    )

    client_id = created.json()["id"]

    response = client.get(f"/api/v1/clients/{client_id}")

    assert response.status_code == 200
    assert response.json()["email"] == "ana@example.com"


def test_update_client(client):
    created = client.post(
        "/api/v1/clients/",
        json={
            "full_name": "Ana Pérez",
            "email": "ana@example.com"
        }
    )

    client_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/clients/{client_id}",
        json={"full_name": "Ana González"}
    )

    assert response.status_code == 200
    assert response.json()["full_name"] == "Ana González"


def test_deactivate_client(client):
    created = client.post(
        "/api/v1/clients/",
        json={
            "full_name": "Ana Pérez",
            "email": "ana@example.com"
        }
    )

    client_id = created.json()["id"]

    response = client.delete(f"/api/v1/clients/{client_id}")

    assert response.status_code == 200

    get_response = client.get(f"/api/v1/clients/{client_id}")

    assert get_response.status_code == 404


def test_duplicate_email(client):
    data = {
        "full_name": "Ana Pérez",
        "email": "ana@example.com"
    }

    first_response = client.post("/api/v1/clients/", json=data)
    second_response = client.post("/api/v1/clients/", json=data)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_invalid_email(client):
    response = client.post(
        "/api/v1/clients/",
        json={
            "full_name": "Ana Pérez",
            "email": "correo-invalido"
        }
    )

    assert response.status_code == 422


def test_list_clients_without_login():
    with TestClient(app) as test_client:
        response = test_client.get("/api/v1/clients/")

        assert response.status_code == 401


def test_client_role_cannot_list_clients(client):
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

    response = client.get("/api/v1/clients/")

    assert response.status_code == 403
