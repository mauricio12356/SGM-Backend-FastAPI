from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import InventoryMovement, Invoice, Sale, SaleDetail, User
from app.repositories import ProductRepository, SaleRepository
from app.schemas import SaleCreate

MONEY = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(MONEY, rounding=ROUND_HALF_UP)


class SaleService:
    def __init__(self) -> None:
        self.sales = SaleRepository()
        self.products = ProductRepository()

    def create(self, db: Session, payload: SaleCreate, cashier: User) -> Sale:
        seen: set[int] = set()
        subtotal = Decimal("0")
        detail_rows: list[tuple] = []

        for line in payload.details:
            if line.product_id in seen:
                raise HTTPException(status_code=422, detail="No repita productos en la misma venta")
            seen.add(line.product_id)
            product = self.products.get(db, line.product_id)
            if product is None or not product.active:
                raise HTTPException(status_code=404, detail=f"Producto {line.product_id} no encontrado")
            if product.current_stock < line.quantity:
                raise HTTPException(
                    status_code=409,
                    detail=f"Stock insuficiente para {product.name}: disponible {product.current_stock}",
                )
            line_subtotal = money(product.sale_price * line.quantity)
            subtotal += line_subtotal
            detail_rows.append((product, line.quantity, product.sale_price, line_subtotal))

        subtotal = money(subtotal)
        tax = money(subtotal * settings.tax_rate)
        total = money(subtotal + tax)
        sale = Sale(
            subtotal=subtotal,
            tax=tax,
            total=total,
            payment_method=payload.payment_method,
            state="COMPLETED",
            cashier_id=cashier.id,
        )
        db.add(sale)
        db.flush()

        for product, quantity, unit_price, line_subtotal in detail_rows:
            previous = product.current_stock
            product.current_stock -= quantity
            sale.details.append(
                SaleDetail(
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=line_subtotal,
                )
            )
            db.add(
                InventoryMovement(
                    movement_type="OUT",
                    quantity=quantity,
                    reference=f"SALE-{sale.id}",
                    previous_stock=previous,
                    new_stock=product.current_stock,
                    product_id=product.id,
                    user_id=cashier.id,
                )
            )

        sale.invoice = Invoice(
            number=f"FAC-{sale.id:08d}",
            customer_name=payload.customer_name,
            customer_tax_id=payload.customer_tax_id,
            subtotal=subtotal,
            tax=tax,
            total=total,
        )
        db.commit()
        return self.sales.get(db, sale.id)  # type: ignore[return-value]

    def cancel(self, db: Session, sale_id: int, user: User) -> Sale:
        sale = self.sales.get(db, sale_id)
        if not sale:
            raise HTTPException(status_code=404, detail="Venta no encontrada")
        if sale.state == "CANCELLED":
            raise HTTPException(status_code=409, detail="La venta ya fue anulada")
        for detail in sale.details:
            product = self.products.get(db, detail.product_id)
            if product:
                previous = product.current_stock
                product.current_stock += detail.quantity
                db.add(
                    InventoryMovement(
                        movement_type="IN",
                        quantity=detail.quantity,
                        reference=f"CANCEL-SALE-{sale.id}",
                        previous_stock=previous,
                        new_stock=product.current_stock,
                        product_id=product.id,
                        user_id=user.id,
                    )
                )
        sale.state = "CANCELLED"
        db.commit()
        return self.sales.get(db, sale.id)  # type: ignore[return-value]
