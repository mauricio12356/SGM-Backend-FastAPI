from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import current_user, require_roles
from app.core.database import get_db
from app.models import Product, User
from app.repositories import ProductRepository
from app.schemas import ProductCreate, ProductRead, ProductUpdate
from app.services import ProductService

router = APIRouter(prefix="/products", tags=["Productos e inventario"])
repo = ProductRepository()
service = ProductService()


@router.get("", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db), _: User = Depends(current_user)) -> list[Product]:
    return repo.list(db)


@router.get("/low-stock", response_model=list[ProductRead])
def low_stock(db: Session = Depends(get_db), _: User = Depends(current_user)) -> list[Product]:
    return repo.low_stock(db)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)
) -> Product:
    product = repo.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@router.post("", response_model=ProductRead, status_code=201)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> Product:
    return service.create(db, payload.model_dump())


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> Product:
    return service.update(db, product_id, payload.model_dump(exclude_unset=True))
