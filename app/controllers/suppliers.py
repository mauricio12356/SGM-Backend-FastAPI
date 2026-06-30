from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.dependencies import current_user, require_roles
from app.core.database import get_db
from app.models import Supplier, User
from app.repositories import SupplierRepository
from app.schemas import SupplierCreate, SupplierRead, SupplierUpdate
from app.services import SupplierService

router = APIRouter(prefix="/suppliers", tags=["Proveedores"])
repo = SupplierRepository()
service = SupplierService()


@router.get("", response_model=list[SupplierRead])
def list_suppliers(db: Session = Depends(get_db), _: User = Depends(current_user)) -> list[Supplier]:
    return repo.list(db)


@router.post("", response_model=SupplierRead, status_code=201)
def create_supplier(
    payload: SupplierCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> Supplier:
    return service.create(db, payload.model_dump())


@router.patch("/{supplier_id}", response_model=SupplierRead)
def update_supplier(
    supplier_id: int,
    payload: SupplierUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> Supplier:
    return service.update(db, supplier_id, payload.model_dump(exclude_unset=True))
