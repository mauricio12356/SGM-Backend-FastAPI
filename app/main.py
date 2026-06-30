from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.controllers import auth, categories, health, products, purchase_orders, reports, sales, suppliers, users
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.services import AuthService


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        AuthService().ensure_default_admin(
            db, settings.default_admin_email, settings.default_admin_password
        )
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "Backend académico para ventas, inventario, usuarios, proveedores, "
        "órdenes de compra, facturación y reportes de un minimercado."
    ),
    lifespan=lifespan,
)

app.include_router(health.router)
for router in (
    auth.router,
    users.router,
    categories.router,
    products.router,
    suppliers.router,
    sales.router,
    purchase_orders.router,
    reports.router,
):
    app.include_router(router, prefix="/api/v1")
