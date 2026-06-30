from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import require_roles
from app.core.database import get_db
from app.models import Sale, User
from app.repositories import SaleRepository
from app.schemas import SaleCreate, SaleRead
from app.services import SaleService

router = APIRouter(prefix="/sales", tags=["Ventas y facturación"])
repo = SaleRepository()
service = SaleService()


@router.get("", response_model=list[SaleRead])
def list_sales(
    db: Session = Depends(get_db), _: User = Depends(require_roles("ADMIN", "CASHIER"))
) -> list[Sale]:
    return repo.list(db)


@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN", "CASHIER")),
) -> Sale:
    sale = repo.get(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return sale


@router.post("", response_model=SaleRead, status_code=201)
def create_sale(
    payload: SaleCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("ADMIN", "CASHIER")),
) -> Sale:
    return service.create(db, payload, user)


@router.post("/{sale_id}/cancel", response_model=SaleRead)
def cancel_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("ADMIN")),
) -> Sale:
    return service.cancel(db, sale_id, user)
