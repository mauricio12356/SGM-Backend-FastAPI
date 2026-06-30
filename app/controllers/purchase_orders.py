from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import require_roles
from app.core.database import get_db
from app.models import PurchaseOrder, User
from app.repositories import PurchaseOrderRepository
from app.schemas import PurchaseOrderCreate, PurchaseOrderRead
from app.services import PurchaseOrderService

router = APIRouter(prefix="/purchase-orders", tags=["Órdenes de compra"])
repo = PurchaseOrderRepository()
service = PurchaseOrderService()


@router.get("", response_model=list[PurchaseOrderRead])
def list_orders(
    db: Session = Depends(get_db), _: User = Depends(require_roles("ADMIN"))
) -> list[PurchaseOrder]:
    return repo.list(db)


@router.get("/{order_id}", response_model=PurchaseOrderRead)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> PurchaseOrder:
    order = repo.get(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order


@router.post("", response_model=PurchaseOrderRead, status_code=201)
def create_order(
    payload: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("ADMIN")),
) -> PurchaseOrder:
    return service.create(db, payload, user)


@router.post("/{order_id}/receive", response_model=PurchaseOrderRead)
def receive_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("ADMIN")),
) -> PurchaseOrder:
    return service.receive(db, order_id, user)
