from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    message: str


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class UserCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=80)
    last_name: str = Field(min_length=2, max_length=80)
    email: str
    password: str = Field(min_length=8)
    role: str = Field(pattern="^(ADMIN|CASHIER)$")


class UserUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=2, max_length=80)
    last_name: str | None = Field(default=None, min_length=2, max_length=80)
    role: str | None = Field(default=None, pattern="^(ADMIN|CASHIER)$")
    active: bool | None = None


class UserRead(ORMModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: str
    active: bool


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = None


class CategoryRead(ORMModel):
    id: int
    name: str
    description: str | None


class ProductCreate(BaseModel):
    barcode: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=2, max_length=120)
    description: str | None = None
    purchase_price: Decimal = Field(ge=0)
    sale_price: Decimal = Field(gt=0)
    current_stock: int = Field(default=0, ge=0)
    minimum_stock: int = Field(default=0, ge=0)
    category_id: int


class ProductUpdate(BaseModel):
    barcode: str | None = Field(default=None, min_length=3, max_length=50)
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = None
    purchase_price: Decimal | None = Field(default=None, ge=0)
    sale_price: Decimal | None = Field(default=None, gt=0)
    minimum_stock: int | None = Field(default=None, ge=0)
    category_id: int | None = None
    active: bool | None = None


class ProductRead(ORMModel):
    id: int
    barcode: str
    name: str
    description: str | None
    purchase_price: Decimal
    sale_price: Decimal
    current_stock: int
    minimum_stock: int
    active: bool
    category_id: int


class SupplierCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    tax_id: str = Field(min_length=10, max_length=20)
    phone: str | None = None
    email: str | None = None
    address: str | None = None


class SupplierUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    active: bool | None = None


class SupplierRead(ORMModel):
    id: int
    name: str
    tax_id: str
    phone: str | None
    email: str | None
    address: str | None
    active: bool


class SaleLineCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class SaleCreate(BaseModel):
    payment_method: str = Field(pattern="^(CASH|CARD)$")
    customer_name: str = "Consumidor final"
    customer_tax_id: str = "9999999999999"
    details: list[SaleLineCreate] = Field(min_length=1)


class SaleDetailRead(ORMModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class InvoiceRead(ORMModel):
    number: str
    issue_date: datetime
    customer_name: str
    customer_tax_id: str
    subtotal: Decimal
    tax: Decimal
    total: Decimal


class SaleRead(ORMModel):
    id: int
    date: datetime
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    payment_method: str
    state: str
    cashier_id: int
    details: list[SaleDetailRead]
    invoice: InvoiceRead | None


class PurchaseOrderLineCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    agreed_price: Decimal = Field(gt=0)


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    details: list[PurchaseOrderLineCreate] = Field(min_length=1)


class PurchaseOrderDetailRead(ORMModel):
    id: int
    product_id: int
    quantity: int
    agreed_price: Decimal
    subtotal: Decimal


class PurchaseOrderRead(ORMModel):
    id: int
    created_at: datetime
    delivery_date: datetime | None
    state: str
    total: Decimal
    supplier_id: int
    administrator_id: int
    details: list[PurchaseOrderDetailRead]


class InventoryMovementRead(ORMModel):
    id: int
    movement_type: str
    quantity: int
    date: datetime
    reference: str | None
    previous_stock: int
    new_stock: int
    product_id: int
    user_id: int


class SalesSummary(BaseModel):
    sales_count: int
    gross_total: Decimal
    tax_total: Decimal
    net_subtotal: Decimal
