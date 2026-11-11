
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security import decode_access_token

import jwt


ACCESS_POLICIES = [
    {
        "path": "/api/v1/ingredients",
        "methods": ["GET"],
        "roles": []
    },
    {
        "path": "/api/v1/ingredients",
        "methods": ["POST", "PATCH", "DELETE"],
        "roles": ["administrador"]
    },
    {
        "path": "/api/v1/clients",
        "methods": ["GET", "POST", "PATCH", "DELETE"],
        "roles": ["administrador"]
    },
    {
        "path": "/api/v1/orders",
        "methods": ["POST"],
        "roles": []
    },
    {
        "path": "/api/v1/orders",
        "methods": ["GET", "PATCH"],
        "roles": ["administrador", "tecnico"]
    },
    {
        "path": "/api/v1/payments",
        "methods": ["POST"],
        "roles": []
    },
    {
        "path": "/api/v1/payments",
        "methods": ["GET"],
        "roles": ["administrador", "tecnico"]
    },
    {
        "path": "/api/v1/auth",
        "methods": ["POST"],
        "roles": []
    },
    {
        "path": "/api/v1/auth/me",
        "methods": ["GET"],
        "roles": ["cliente", "tecnico", "administrador"]
    }
]


def get_required_roles(path: str, method: str):
    for policy in ACCESS_POLICIES:
        base_path = policy["path"]

        matches_path = (
            path == base_path
            or path.startswith(base_path + "/")
        )

        if matches_path and method in policy["methods"]:
            return policy["roles"]

    return None


class GatewayPolicyMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method.upper()

        required_roles = get_required_roles(path, method)

        # Las rutas sin política definida continúan hacia FastAPI.
        if required_roles is None:
            return await call_next(request)

        # Las rutas públicas no requieren autenticación.
        if required_roles == []:
            return await call_next(request)

        token = request.cookies.get("access_token")

        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Debe iniciar sesión"}
            )

        try:
            payload = decode_access_token(token)
            user_role = payload.get("role")

            if not user_role:
                raise ValueError("El token no contiene un rol")

        except (jwt.InvalidTokenError, ValueError, KeyError):
            return JSONResponse(
                status_code=401,
                content={"detail": "Sesión inválida o expirada"}
            )

        if user_role not in required_roles:
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "No tiene permisos para acceder a este recurso"
                }
            )

        return await call_next(request)
