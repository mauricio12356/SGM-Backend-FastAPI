from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models import Category, Product, Supplier, User
from app.repositories import CategoryRepository, ProductRepository, SupplierRepository, UserRepository


def not_found(resource: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{resource} no encontrado")


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepository()

    def create(self, db: Session, data: dict) -> User:
        if self.repo.by_email(db, data["email"]):
            raise HTTPException(status_code=409, detail="El correo ya está registrado")
        payload = data.copy()
        payload["password_hash"] = hash_password(payload.pop("password"))
        try:
            user = self.repo.create(db, payload)
            db.commit()
            return user
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(status_code=409, detail="No se pudo registrar el usuario") from exc

    def update(self, db: Session, user_id: int, data: dict) -> User:
        user = self.repo.get(db, user_id)
        if not user:
            raise not_found("Usuario")
        user = self.repo.update(db, user, data)
        db.commit()
        return user


class CategoryService:
    def __init__(self) -> None:
        self.repo = CategoryRepository()

    def create(self, db: Session, data: dict) -> Category:
        if self.repo.by_name(db, data["name"]):
            raise HTTPException(status_code=409, detail="La categoría ya existe")
        category = self.repo.create(db, data)
        db.commit()
        return category

    def update(self, db: Session, category_id: int, data: dict) -> Category:
        category = self.repo.get(db, category_id)
        if not category:
            raise not_found("Categoría")
        category = self.repo.update(db, category, data)
        db.commit()
        return category

    def delete(self, db: Session, category_id: int) -> None:
        category = self.repo.get(db, category_id)
        if not category:
            raise not_found("Categoría")
        if category.products:
            raise HTTPException(status_code=409, detail="No se puede eliminar una categoría con productos")
        self.repo.delete(db, category)
        db.commit()


class ProductService:
    def __init__(self) -> None:
        self.repo = ProductRepository()
        self.categories = CategoryRepository()

    def create(self, db: Session, data: dict) -> Product:
        if not self.categories.get(db, data["category_id"]):
            raise not_found("Categoría")
        if self.repo.by_barcode(db, data["barcode"]):
            raise HTTPException(status_code=409, detail="El código de barras ya existe")
        product = self.repo.create(db, data)
        db.commit()
        return product

    def update(self, db: Session, product_id: int, data: dict) -> Product:
        product = self.repo.get(db, product_id)
        if not product:
            raise not_found("Producto")
        if "category_id" in data and not self.categories.get(db, data["category_id"]):
            raise not_found("Categoría")
        product = self.repo.update(db, product, data)
        db.commit()
        return product


class SupplierService:
    def __init__(self) -> None:
        self.repo = SupplierRepository()

    def create(self, db: Session, data: dict) -> Supplier:
        if self.repo.by_tax_id(db, data["tax_id"]):
            raise HTTPException(status_code=409, detail="El RUC/identificación ya existe")
        supplier = self.repo.create(db, data)
        db.commit()
        return supplier

    def update(self, db: Session, supplier_id: int, data: dict) -> Supplier:
        supplier = self.repo.get(db, supplier_id)
        if not supplier:
            raise not_found("Proveedor")
        supplier = self.repo.update(db, supplier, data)
        db.commit()
        return supplier
