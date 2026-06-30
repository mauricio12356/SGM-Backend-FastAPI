from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80))
    last_name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(300))
    role: Mapped[str] = mapped_column(String(20), default="CASHIER")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    sales: Mapped[list[Sale]] = relationship(back_populates="cashier")
    purchase_orders: Mapped[list[PurchaseOrder]] = relationship(back_populates="administrator")
    inventory_movements: Mapped[list[InventoryMovement]] = relationship(back_populates="user")
    tokens: Mapped[list[AuthToken]] = relationship(back_populates="user", cascade="all, delete-orphan")


class AuthToken(Base):
    __tablename__ = "auth_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(back_populates="tokens")


# Catalogo de productos
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    products: Mapped[list[Product]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    barcode: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    purchase_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    sale_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    current_stock: Mapped[int] = mapped_column(Integer, default=0)
    minimum_stock: Mapped[int] = mapped_column(Integer, default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped[Category] = relationship(back_populates="products")
    sale_details: Mapped[list[SaleDetail]] = relationship(back_populates="product")
    order_details: Mapped[list[PurchaseOrderDetail]] = relationship(back_populates="product")
    inventory_movements: Mapped[list[InventoryMovement]] = relationship(back_populates="product")


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    tax_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    address: Mapped[str | None] = mapped_column(String(250), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    purchase_orders: Mapped[list[PurchaseOrder]] = relationship(back_populates="supplier")


# Ventas y facturacion
class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    tax: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    payment_method: Mapped[str] = mapped_column(String(20))
    state: Mapped[str] = mapped_column(String(20), default="COMPLETED")
    cashier_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    cashier: Mapped[User] = relationship(back_populates="sales")
    details: Mapped[list[SaleDetail]] = relationship(
        back_populates="sale", cascade="all, delete-orphan", lazy="selectin"
    )
    invoice: Mapped[Invoice | None] = relationship(
        back_populates="sale", uselist=False, cascade="all, delete-orphan", lazy="selectin"
    )


class SaleDetail(Base):
    __tablename__ = "sale_details"
    __table_args__ = (UniqueConstraint("sale_id", "product_id", name="uq_sale_product"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    sale: Mapped[Sale] = relationship(back_populates="details")
    product: Mapped[Product] = relationship(back_populates="sale_details", lazy="joined")


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    issue_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    customer_name: Mapped[str] = mapped_column(String(150), default="Consumidor final")
    customer_tax_id: Mapped[str] = mapped_column(String(20), default="9999999999999")
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    tax: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"), unique=True)

    sale: Mapped[Sale] = relationship(back_populates="invoice")


# Compras e inventario
class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    delivery_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    state: Mapped[str] = mapped_column(String(30), default="PENDING")
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    administrator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    supplier: Mapped[Supplier] = relationship(back_populates="purchase_orders", lazy="joined")
    administrator: Mapped[User] = relationship(back_populates="purchase_orders", lazy="joined")
    details: Mapped[list[PurchaseOrderDetail]] = relationship(
        back_populates="order", cascade="all, delete-orphan", lazy="selectin"
    )


class PurchaseOrderDetail(Base):
    __tablename__ = "purchase_order_details"
    __table_args__ = (UniqueConstraint("order_id", "product_id", name="uq_order_product"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer)
    agreed_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    order_id: Mapped[int] = mapped_column(ForeignKey("purchase_orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    order: Mapped[PurchaseOrder] = relationship(back_populates="details")
    product: Mapped[Product] = relationship(back_populates="order_details", lazy="joined")


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id: Mapped[int] = mapped_column(primary_key=True)
    movement_type: Mapped[str] = mapped_column(String(20))
    quantity: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    reference: Mapped[str | None] = mapped_column(String(120), nullable=True)
    previous_stock: Mapped[int] = mapped_column(Integer)
    new_stock: Mapped[int] = mapped_column(Integer)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    product: Mapped[Product] = relationship(back_populates="inventory_movements", lazy="joined")
    user: Mapped[User] = relationship(back_populates="inventory_movements", lazy="joined")
