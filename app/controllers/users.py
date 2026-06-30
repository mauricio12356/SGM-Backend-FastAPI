from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.dependencies import require_roles
from app.core.database import get_db
from app.models import User
from app.repositories import UserRepository
from app.schemas import UserCreate, UserRead, UserUpdate
from app.services import UserService

router = APIRouter(prefix="/users", tags=["Usuarios"])
repo = UserRepository()
service = UserService()


@router.get("", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db), _: User = Depends(require_roles("ADMIN"))
) -> list[User]:
    return repo.list(db)


@router.post("", response_model=UserRead, status_code=201)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> User:
    return service.create(db, payload.model_dump())


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> User:
    return service.update(db, user_id, payload.model_dump(exclude_unset=True))
