import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
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
        yield test_client

    Base.metadata.drop_all(bind=test_engine)


def user_data():
    return {
        "full_name": "Ana Pérez",
        "email": "ana@example.com",
        "password": "FreshBowl123"
    }


def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json=user_data()
    )

    assert response.status_code == 201
    assert response.json()["email"] == "ana@example.com"
    assert response.json()["role"] == "cliente"
    assert "password_hash" not in response.json()


def test_duplicate_registration(client):
    client.post(
        "/api/v1/auth/register",
        json=user_data()
    )

    response = client.post(
        "/api/v1/auth/register",
        json=user_data()
    )

    assert response.status_code == 409


def test_login_user(client):
    client.post(
        "/api/v1/auth/register",
        json=user_data()
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "ana@example.com",
            "password": "FreshBowl123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.cookies


def test_login_invalid_password(client):
    client.post(
        "/api/v1/auth/register",
        json=user_data()
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "ana@example.com",
            "password": "incorrecta"
        }
    )

    assert response.status_code == 401


def test_get_profile_authenticated(client):
    client.post(
        "/api/v1/auth/register",
        json=user_data()
    )

    client.post(
        "/api/v1/auth/login",
        json={
            "email": "ana@example.com",
            "password": "FreshBowl123"
        }
    )

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 200
    assert response.json()["email"] == "ana@example.com"


def test_get_profile_without_login(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_logout(client):
    client.post(
        "/api/v1/auth/register",
        json=user_data()
    )

    client.post(
        "/api/v1/auth/login",
        json={
            "email": "ana@example.com",
            "password": "FreshBowl123"
        }
    )

    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 200

    profile_response = client.get("/api/v1/auth/me")

    assert profile_response.status_code == 401