from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.controllers.dependencies import require_roles
from app.core.database import get_db
from app.models import InventoryMovement, Sale, User
from app.schemas import InventoryMovementRead, SalesSummary

router = APIRouter(prefix="/reports", tags=["Reportes"])


@router.get("/sales-summary", response_model=SalesSummary)
def sales_summary(
    db: Session = Depends(get_db), _: User = Depends(require_roles("ADMIN"))
) -> SalesSummary:
    row = db.execute(
        select(
            func.count(Sale.id),
            func.coalesce(func.sum(Sale.total), 0),
            func.coalesce(func.sum(Sale.tax), 0),
            func.coalesce(func.sum(Sale.subtotal), 0),
        ).where(Sale.state == "COMPLETED")
    ).one()
    return SalesSummary(
        sales_count=row[0],
        gross_total=Decimal(row[1]),
        tax_total=Decimal(row[2]),
        net_subtotal=Decimal(row[3]),
    )


@router.get("/inventory-movements", response_model=list[InventoryMovementRead])
def inventory_movements(
    db: Session = Depends(get_db), _: User = Depends(require_roles("ADMIN"))
) -> list[InventoryMovement]:
    return list(db.scalars(select(InventoryMovement).order_by(InventoryMovement.date.desc()).limit(500)))
