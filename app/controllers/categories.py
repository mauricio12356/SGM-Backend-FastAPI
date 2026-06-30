from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.controllers.dependencies import current_user, require_roles
from app.core.database import get_db
from app.models import Category, User
from app.repositories import CategoryRepository
from app.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.services import CategoryService

router = APIRouter(prefix="/categories", tags=["Categorías"])
repo = CategoryRepository()
service = CategoryService()


@router.get("", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db), _: User = Depends(current_user)) -> list[Category]:
    return repo.list(db)


@router.post("", response_model=CategoryRead, status_code=201)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> Category:
    return service.create(db, payload.model_dump())


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> Category:
    return service.update(db, category_id, payload.model_dump(exclude_unset=True))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> Response:
    service.delete(db, category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
