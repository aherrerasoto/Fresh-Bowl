
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_consultar_pagos_sin_autenticacion(client):
    response = client.get("/api/v1/payments/")

    assert response.status_code == 401


def test_cliente_no_puede_consultar_pagos(client):
    # Registrar un cliente.
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Cliente de prueba",
            "email": "cliente@test.com",
            "password": "ClavePrueba123"
        }
    )

    assert register_response.status_code in (200, 201)

    # Iniciar sesión como cliente.
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "cliente@test.com",
            "password": "ClavePrueba123"
        }
    )

    assert login_response.status_code == 200

    # Intentar consultar los pagos.
    response = client.get("/api/v1/payments/")

    assert response.status_code == 403
