from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models import (
    AuthToken,
    Category,
    InventoryMovement,
    Product,
    PurchaseOrder,
    Sale,
    Supplier,
    User,
)
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    def by_email(self, db: Session, email: str) -> User | None:
        return db.scalar(select(User).where(func.lower(User.email) == email.lower()))


class TokenRepository(BaseRepository[AuthToken]):
    def __init__(self) -> None:
        super().__init__(AuthToken)

    def valid_token(self, db: Session, token: str) -> AuthToken | None:
        now = datetime.now(UTC)
        return db.scalar(
            select(AuthToken)
            .options(selectinload(AuthToken.user))
            .where(AuthToken.token == token, AuthToken.expires_at > now)
        )


class CategoryRepository(BaseRepository[Category]):
    def __init__(self) -> None:
        super().__init__(Category)

    def by_name(self, db: Session, name: str) -> Category | None:
        return db.scalar(select(Category).where(func.lower(Category.name) == name.lower()))


class ProductRepository(BaseRepository[Product]):
    def __init__(self) -> None:
        super().__init__(Product)

    def by_barcode(self, db: Session, barcode: str) -> Product | None:
        return db.scalar(select(Product).where(Product.barcode == barcode))

    def low_stock(self, db: Session) -> list[Product]:
        return list(
            db.scalars(
                select(Product)
                .where(Product.active.is_(True), Product.current_stock <= Product.minimum_stock)
                .order_by(Product.current_stock.asc())
            )
        )


class SupplierRepository(BaseRepository[Supplier]):
    def __init__(self) -> None:
        super().__init__(Supplier)

    def by_tax_id(self, db: Session, tax_id: str) -> Supplier | None:
        return db.scalar(select(Supplier).where(Supplier.tax_id == tax_id))


class SaleRepository(BaseRepository[Sale]):
    def __init__(self) -> None:
        super().__init__(Sale)

    def get(self, db: Session, object_id: int) -> Sale | None:
        return db.scalar(
            select(Sale)
            .options(selectinload(Sale.details), selectinload(Sale.invoice))
            .where(Sale.id == object_id)
        )

    def list(self, db: Session, *, offset: int = 0, limit: int = 100) -> list[Sale]:
        return list(
            db.scalars(
                select(Sale)
                .options(selectinload(Sale.details), selectinload(Sale.invoice))
                .order_by(Sale.date.desc())
                .offset(offset)
                .limit(limit)
            )
        )


class PurchaseOrderRepository(BaseRepository[PurchaseOrder]):
    def __init__(self) -> None:
        super().__init__(PurchaseOrder)

    def get(self, db: Session, object_id: int) -> PurchaseOrder | None:
        return db.scalar(
            select(PurchaseOrder)
            .options(selectinload(PurchaseOrder.details))
            .where(PurchaseOrder.id == object_id)
        )


class InventoryRepository(BaseRepository[InventoryMovement]):
    def __init__(self) -> None:
        super().__init__(InventoryMovement)
