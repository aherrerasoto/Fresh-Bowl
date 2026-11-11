
from fastapi.testclient import TestClient

from app.main import app
from app.gateway.policies import (
    ACCESS_POLICIES,
    get_required_roles
)


def test_gateway_status():
    with TestClient(app) as client:
        response = client.get("/api/v1/gateway/status")

    assert response.status_code == 200
    assert response.json()["status"] == "active"
    assert response.json()["gateway"] == "Fresh Bowl API Gateway"


def test_gateway_policies():
    with TestClient(app) as client:
        response = client.get("/api/v1/gateway/policies")

    assert response.status_code == 200
    assert len(response.json()["policies"]) == len(ACCESS_POLICIES)


def test_public_ingredient_route():
    roles = get_required_roles(
        "/api/v1/ingredients/",
        "GET"
    )

    assert roles == []


def test_admin_can_manage_ingredients():
    roles = get_required_roles(
        "/api/v1/ingredients/",
        "POST"
    )

    assert roles == ["administrador"]


def test_orders_require_authorized_role():
    roles = get_required_roles(
        "/api/v1/orders/",
        "GET"
    )

    assert roles == ["administrador", "tecnico"]


def test_guest_can_create_orders():
    roles = get_required_roles(
        "/api/v1/orders/",
        "POST"
    )

    assert roles == []


def test_payments_require_authorized_role():
    roles = get_required_roles(
        "/api/v1/payments/",
        "GET"
    )

    assert roles == ["administrador", "tecnico"]


def test_unknown_route_has_no_gateway_policy():
    roles = get_required_roles(
        "/api/v1/unknown/",
        "GET"
    )

    assert roles is None
