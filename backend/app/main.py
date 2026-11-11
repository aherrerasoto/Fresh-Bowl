from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine

from app.inventory import models as inventory_models
from app.clients import models as client_models
from app.orders import models as order_models
from app.payments import models as payment_models
from app.auth import models as auth_models

from app.inventory.routes import router as inventory_router
from app.clients.routes import router as clients_router
from app.orders.routes import router as orders_router
from app.payments.routes import router as payments_router
from app.auth.routes import router as auth_router
from app.gateway.routes import router as gateway_router
from app.graphql.routes import router as graphql_router

from app.gateway.policies import GatewayPolicyMiddleware


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend del sistema Fresh Bowl"
)

Base.metadata.create_all(bind=engine)

app.add_middleware(GatewayPolicyMiddleware)

app.include_router(inventory_router, prefix="/api/v1")
app.include_router(clients_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")
app.include_router(payments_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(gateway_router, prefix="/api/v1")
app.include_router(graphql_router, prefix="/api/v1")


@app.get("/")
def inicio():
    return {
        "message": "Bienvenido a Fresh Bowl API",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}