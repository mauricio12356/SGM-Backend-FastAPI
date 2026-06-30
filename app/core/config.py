from __future__ import annotations

import os
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Sistema de Gestion de Minimercado")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./sgm.db")
    tax_rate: Decimal = Decimal(os.getenv("TAX_RATE", "0.15"))
    default_admin_email: str = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@sgm.local")
    default_admin_password: str = os.getenv("DEFAULT_ADMIN_PASSWORD", "Admin123*")


settings = Settings()
